def api_get_user_info(request):
    """获取用户信息"""
    username = request.GET.get("username")  # str
    # TODO 从数据库中获取用户信息


def api_update_user_info(request):
    """更新用户信息"""
    changes = request.POST.get("changes")  # json
    # TODO 更新数据库中的用户信息


def api_get_user_list(request):
    """获取用户列表"""
    # TODO 从数据库中获取用户列表
