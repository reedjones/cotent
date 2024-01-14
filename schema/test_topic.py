from unittest import TestCase
from django.test import TestCase
from django.urls import reverse
from .topic import Topic, Category, Content, TopicIndexView, CategoryIndexView, ContentDetailView

data = {
  "mainTopics": [
    {
      "name": "Art",
      "subcategories": [
        "Drawing",
        "Painting",
        "Digital_Art"
      ]
    },
    {
      "name": "Music",
      "subcategories": [
        "Classical",
        "Jazz",
        "Rock",
        "Electronic"
      ]
    },
    {
      "name": "Programming",
      "subcategories": [
        "Python",
        "JavaScript",
        "Java",
        "C++"
      ]
    },
    {
      "name": "Business",
      "subcategories": [
        "Entrepreneurship",
        "Freelancing",
        "Marketing",
        "Finance"
      ]
    },
    {
      "name": "Philosophy",
      "subcategories": [
        "Ethics",
        "Epistemology",
        "Metaphysics"
      ]
    },
    {
      "name": "Theories_and_Ideas",
      "subcategories": [
        "Scientific_Theories",
        "Social_Theories",
        "Mathematical_Concepts",
        "Political_Theories"
      ]
    },
    {
      "name": "Literature",
      "subcategories": [
        "Literary_Genres",
        "Authors",
        "Book_Reviews",
        "Literary_Analysis"
      ]
    },
    {
      "name": "Media",
      "subcategories": [
        "Film",
        "Television",
        "Digital_Media",
        "Gaming",
        "Media_Production"
      ]
    },
    {
      "name": "Design",
      "subcategories": [
        "Graphic_Design",
        "Web_Design",
        "Interior_Design",
        "Product_Design"
      ]
    },
    {
      "name": "Politics",
      "subcategories": [
        "Political_Ideologies",
        "Political_Movements",
        "Political_Commentary",
        "International_Relations"
      ]
    },
    {
      "name": "Personal_Journal",
      "subcategories": [
        "Dreams",
        "Goals",
        "Tasks"
      ]
    },
    {
      "name": "Notes",
      "subcategories": [
        "Brain_in_a_vat",
        "Ikigai",
        "The_Mothers_Eye",
        "Cyber_Punk_Future_Clothes",
        "Harper_Note",
        "Highway_Cameras_California",
        "Measurable_Space",
        "Now",
        "Osasis_Notes_and_Quotes",
        "Conscious_Agents_in_Langchain",
        "Information_Weekly",
        "Mythology_Machine",
        "Python_Thornizer"
      ]
    },
    {
      "name": "PersonalProjects",
      "subcategories": [
        "IdeaLand",
        "Poetry",
        "Web_Management"
      ]
    },
    {
      "name": "Prompts",
      "subcategories": [
        "Affirmation_Life_Energies",
        "Application_Generator_Prompt",
        "Case_Study_Helper_Prompt",
        "Futures_Not_So_Bright",
        "List_Output_Handles_Recursion"
      ]
    },
    {
      "name": "Research",
      "subcategories": [
        "Memetics",
        "Music_Research",
        "OSINT",
        "News_Notes"
      ]
    },
    {
      "name": "Tips_and_Bits",
      "subcategories": [
        "Python"
      ]
    },
    {
      "name": "Unsorted",
      "subcategories": [
        "The_Conspiracy"
      ]
    },
    {
      "name": "ValueContent",
      "subcategories": [
        "Email_Anxiety",
        "Topics",
        "Value_Creation_Through_Content"
      ]
    },
    {
      "name": "Week_Planner",
      "subcategories": [
        "Inbox"
      ]
    },
    {
      "name": "StackEditDump",
      "subcategories": [
        "12_16_Notes_Parenting",
        "Waking_Life_Quotes"
      ]
    },
    {
      "name": "Diary",
      "subcategories": [
        20230725,
        "DreamJournal",
        "Learned"
      ]
    },
    {
      "name": "Scripts",
      "subcategories": [
        "Scripts_1"
      ]
    }
  ]
}

from django.utils.text import slugify
class Test(TestCase):
    def setUp(self):
        self.topics = []
        self.categories = []
        self.contents = []
        for item in data['mainTopics']:
            topic = Topic(name=item['name'])
            self.topics.append(topic)
            for subcategory in item['subcategories']:
                category = Category(topic=topic, name=subcategory)
                self.categories.append(category)
                content = Content(category=category,
                               content_type=slugify(subcategory).replace("-", "_"),
                               object_id=1,
                               uid_type='slug',
                               uid='sample-slug'
                               )
                self.contents.append(content)

        # Create sample data for testing
            #
        for created in [] + self.categories + self.contents + self.topics:
            print(f"Created ({type(created)}): {created}")

        # Create instances of your views
    def test_topic_model(self):
        for topic in self.topics:
            print(f"Testing Topic: {topic}")
            print(f"{topic.name} | {topic.get_absolute_url()} | {topic.slug} | {topic.get_category_url()}")
            self.assertEqual(topic.name, topic.name)
            self.assertEqual(topic.slug, slugify(topic.name))
            self.assertEqual(topic.get_absolute_url(), f"/topics/{topic.slug}/")
            self.assertEqual(topic.get_category_url(), f"/topics/{topic.slug}/categories/")

    def test_category_model(self):
        for category in self.categories:
            print(f"Testing Category: {category}")
            print(f"{category.name} | {category.slug} | {category.topic.name} | {category.topic.slug} | {category.topic.get_absolute_url()}")
            self.assertEqual(category.name, category.name)
            self.assertEqual(category.slug, slugify(category.name))
            self.assertEqual(category.get_absolute_url(), f"/topics/{category.topic.slug}/categories/{category.slug}/")
            # self.assertEqual(category.get_content_url(), f"/topics/{category.topic.slug}/categories/{category.slug}/contents/")

    def test_content_model(self):
        for content in self.contents:
            print(f"Testing Content: {content}")
            print(f"ct: {content.content_type} | object_id: {content.object_id} | uid_type: {content.uid_type} | uid: {content.uid}")
            print(f"url: {content.get_absolute_url()}")
            self.assertEqual(content.content_type, content.content_type)
            self.assertEqual(content.object_id, content.object_id)
            self.assertEqual(content.uid_type, content.uid_type)
            self.assertEqual(content.uid, content.uid)
            self.assertEqual(content.get_absolute_url(), f"/topics/{content.category.topic.slug}/categories/{content.category.slug}/{content.content_type_slug}::{content.uid_slug}/")
            # self.assertEqual(content.get_content_url(), f"/topics/{content.category.topic.slug}/categories/{content.category.slug}/contents/")
            # self.assertEqual(content.get_content_url(), f"/topics/{content.category.topic.slug}/categories/{content.category.slug}/contents/")
            # self.assertEqual(content.get_content_url(), f"/topics/{content.category.topic.slug}/categories/{content.category.slug}/contents/")


    def test_topic_index_view(self):
        # # Test your TopicIndexView class
        # response = self.client.get(reverse('topic_list'))
        # # Adjust the reverse() based on your actual URL configuration
        # self.assertEqual(response.status_code, 200)  # Replace 200 with the expected status code
        pass
        # Add more assertions based on your view logic

    def test_category_index_view(self):

        # Test your CategoryIndexView class
        # response = self.client.get(
        #     reverse('topic_category_list', kwargs={'topic_slug': self.topic.slug, 'category_slug': self.category.slug}))
        # self.assertEqual(response.status_code, 200)  # Replace 200 with the expected status code
        pass
        # Add more assertions based on your view logic

    def test_content_detail_view(self):
        # # Test your ContentDetailView class
        # response = self.client.get(reverse('topic_category_detail',
        #                                    kwargs={'topic_slug': self.topic.slug, 'category_slug': self.category.slug,
        #                                            'content_type_slug': self.content.content_type,
        #                                            'content_id': self.content.id}))
        # self.assertEqual(response.status_code, 200)  # Replace 200 with the expected status code
        pass
        # Add more assertions based on your view logic
