from abc import abstractmethod, ABC
from dataclasses import dataclass
from types import FunctionType
from typing import Any, Union, List
from django.contrib.contenttypes.models import ContentType
from django.db import models
import enum
from urllib.parse import unquote
from urllib.parse import quote
from django.utils.http import urlencode
from django.utils.text import slugify

from django.urls import path


class DetailViewType(enum.Enum):
    full = 'full'
    focus = 'focus'
    summary = 'summary'
    gallery = 'gallery'
    article = 'article'
    video = 'video'
    audio = 'audio'
    image = 'image'
    document = 'document'
    quote = 'quote'
    link = 'link'
    code = 'code'


class ListViewType(enum.Enum):
    list = 'list'
    grid = 'grid'


class UidTypeChoice(enum.Enum):
    slug = "slug"
    big_integer = "big_integer"
    char = "char"
    uuid = "uuid"

    @classmethod
    def from_django_model_field_type(cls, field_type: Any) -> "UidTypeChoice":
        return {
            models.SlugField: cls.slug,
            models.BigIntegerField: cls.big_integer,
            models.CharField: cls.char,
            models.UUIDField: cls.uuid,
        }[field_type]

    def to_django_model_field_type(self) -> Any:
        return {
            UidTypeChoice.slug: models.SlugField,
            UidTypeChoice.big_integer: models.BigIntegerField,
            UidTypeChoice.char: models.CharField,
            UidTypeChoice.uuid: models.UUIDField,
        }[self]


class PageTypeable(ABC):
    global_view_params = ["view_type", "display_options"]

    global_view_param_dict = dict.fromkeys(global_view_params, None)

    @abstractmethod
    def get_page_types(self) -> List[Any]:
        raise NotImplementedError


def url_str_to_django_path(url_str: str, view_function: FunctionType):
    """
    Takes a str (generated from `get_url`) and creates an entry for django.urlpatterns using django.urls.path
    :param url_str: str
    :return: django.urls.resolvers.URLPattern
    --------
    ```python
    # Example usage:
    url_str = "/topics/my_topic/my_category/my_content_type::my_uid/"
    django_path = url_str_to_django_path(url_str)
    ```
    --------
    """
    parts = url_str.strip('/').split('/')
    path_components = []

    for part in parts:
        if '::' in part:
            # Handle content type and UID
            content_type, uid = part.split('::')
            path_components.append(f'<str:{content_type}>::<{uid}>')
        else:
            path_components.append(part)

    # Create the Django path
    path_str = '/'.join(path_components)
    return path(path_str, view_function)  # Replace your_view_function with the actual view function


def template_path_isvalid(templates_path: str, template_name: str):
    """
    Checks if the template path is valid
    :param templates_path:
    :param template_name:
    :return:
    """
    pass


class ListViewable(PageTypeable):
    view_type: ListViewType = ListViewType.grid

    def get_page_types(self) -> List[ListViewType]:
        return [e for e in ListViewType]

    def get_page_type_names(self) -> List[str]:
        return [e.value for e in ListViewType]


class DetailViewable(PageTypeable):
    view_type: DetailViewType = DetailViewType.full

    def get_page_types(self) -> List[Any]:
        return [e for e in DetailViewType]

    def get_page_type_names(self) -> List[str]:
        return [e.value for e in DetailViewType]


@dataclass
class Topic:
    name: str

    def get_template_names(self):
        return [f"topics/{self.slug}.html", self.default_template_name]

    def template_name(self):
        return f"topics/{self.slug}.html"

    default_template_name = "topics/default.html"

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/topics/{self.slug}/"

    def get_category_url(self):
        return f"/topics/{self.slug}/categories/"


@dataclass
class Category:
    topic: Topic
    name: str

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return f"{self.topic.name}/{self.name}"

    def get_category_content_url(self):
        pass

    def get_category_content_detail_url(self):
        pass

    def get_absolute_url(self):
        return f"/topics/{self.topic.slug}/categories/{self.slug}/"


@dataclass
class Content:
    category: Category
    content_type: Union[ContentType, str]
    object_id: int
    uid_type: Union[UidTypeChoice, str]
    uid: Union[str, models.BigIntegerField, models.UUIDField, models.CharField, models.SlugField]

    def get_content_url(self):
        pass

    @property
    def content_type_slug(self):
        try:
            return slugify(self.resolve_content_type().name)
        except (AttributeError, ContentType.DoesNotExist) as e:
            print(e)
            return slugify(self.content_type)

    @property
    def object_id_slug(self):
        return urlencode(str(self.object_id))

    @property
    def uid_slug(self):

        return quote(str(self.uid))

        #return urlencode(self.uid)

    def get_content_detail_url(self):
        pass

    @classmethod
    def resolve_uid_type_from_url(cls, url_value):
        return UidTypeChoice[unquote(url_value)]

    def resolve_uid_type(self):
        if isinstance(self.uid_type, str):
            return UidTypeChoice[self.uid_type]
        else:
            return self.uid_type

    def resolve_content_type(self):
        if isinstance(self.content_type, str):
            return ContentType.objects.get(app_label=self.content_type)
        else:
            return self.content_type

    @property
    def content_object(self) -> models.Model:
        return self.content_type.model_class().objects.get(id=self.object_id)

    def __str__(self):
        return f"{self.content_type}::{self.uid}"

    def get_absolute_url(self):
        return f"/topics/{self.category.topic.slug}/" \
               f"categories/{self.category.slug}/" \
               f"{self.content_type_slug}::{self.uid_slug}/"


@dataclass
class TopicIndexView(ListViewable):
    # Implement other methods or attributes specific to this class
    topic: Topic

    def get_url(self):
        return f"/topics/{self.topic.name}/"

    @property
    def default_template_name(self):
        return "topics/topic_index.html"

    def get_template_names(self):
        return [f"topics/{self.topic.name}.html", self.default_template_name]

    def __str__(self):
        return f"TopicIndexView for topic {self.topic.name}"


@dataclass
class CategoryIndexView(ListViewable):
    # Implement other methods or attributes specific to this class
    category: Category

    def get_url(self):
        return f"/topics/{self.category.topic.name}/{self.category.name}/"

    @property
    def default_template_name(self):
        return "topics/category_index.html"

    def get_template_names(self):
        return [f"topics/{self.category.topic.name}/{self.category.name}.html", self.default_template_name]

    def __str__(self):
        return f"CategoryIndexView for category {self.category.name}"


@dataclass
class ContentDetailView(DetailViewable):
    # Implement other methods or attributes specific to this class
    content: Content

    def get_url(self):
        return f"/topics/{self.content.category.topic.name}/{self.content.category.name}/{self.content.content_type}::{self.content.uid}/"

    @property
    def default_template_name(self):
        return "topics/content_detail.html"

    def get_template_names(self):
        return [
            f"topics/{self.content.category.topic.name}/{self.content.category.name}/{self.content.content_type}::{self.content.uid}.html",
            self.default_template_name]

    def __str__(self):
        return f"ContentDetailView for content {self.content}"
