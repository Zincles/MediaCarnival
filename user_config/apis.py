import json
from django.http import HttpResponse
from user_config.models import UserConfig


## 获取用户的当前配置
def get_user_config(request):
    
    # 获取当前用户的配置
    user_config :UserConfig = request.user.user_config
    return HttpResponse(json.dumps(user_config.__dict__))
