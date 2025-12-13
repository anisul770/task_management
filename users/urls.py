from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,admin_dashboard,assign_role,create_group,group_list,CustomLoginView,ProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordResetConfirmView,EditProfileView,ViewGroup,CreateGroup,SignUpView,AssignRole,AdminDashboard
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView


urlpatterns = [
    # path('sign-up/',sign_up,name='sign-up'),
    path('sign-up/',SignUpView.as_view(),name='sign-up'),
    # path('sign-in/',sign_in,name='sign-in'),
    path('sign-in/',CustomLoginView.as_view(),name='sign-in'),
    # path('sign_out/',sign_out,name='sign-out'),
    path('sign_out/',LogoutView.as_view(),name='sign-out'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    # path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin/dashboard/',AdminDashboard.as_view(),name='admin-dashboard'),
    # path('admin/<int:user_id>/assign-role',assign_role,name='assign-role'),
    path('admin/<int:user_id>/assign-role',AssignRole.as_view(),name='assign-role'),
    # path('admin/create_group',create_group,name='create-group'),
    path('admin/create_group',CreateGroup.as_view(),name='create-group'),
    # path('admin/group-list/',group_list,name='group-list'),
    path('admin/group-list/',ViewGroup.as_view(),name='group-list'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('password_change/',ChangePassword.as_view(),name='password-change'),
    path('password_change/done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    path('password_reset/',CustomPasswordResetView.as_view(),name="password-reset"),
    path('password_reset/confirm/<uidb64>/<token>',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('edit-profile/',EditProfileView.as_view(),name='edit_profile')
]
