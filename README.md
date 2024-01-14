Generic django-app for content modeling Topic, Category, and Content schemas. 

# URL Schema
url_schema:
  /<str:topic_id>/<str:category_id>/<str:content_type_id>::<int_or_str:content_id>/

# Global Parameters
global_get_param_schema:
  view::<str:view_type_id>

# URL Example
url_example:
  /art  /paintings  /painting::the%20mona%20lisa  /gallery 

# Hierarchy/Global Params/View Routing/View Arguments
hierarchy/global_params/view_routing/view_arguments:
  - /art                                       ?              ->   topic_list            ((default) view_type)
  - /art/                                      ?view::list    ->   topic_list            ((list) view_type)
  - /art /paintings                            ?              ->   topic_category_list   ((default) view_type) 
  - /art /paintings                            ?view::grid    ->   topic_category_list   ((grid) view_type)                               
  - /art /paintings /painting::the mona lisa   ?              ->   topic_category_detail  ((default) view_type) 
  - /art /paintings /painting:: the mona lisa  ?view::gallery ->   topic_category_detail  ((gallery) view_type) 
