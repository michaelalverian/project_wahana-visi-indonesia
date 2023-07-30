from django.urls import path

from wvi.views.authentication_views import CustomAuthentication
from wvi.views.child_views import ChildView
from wvi.views.child_record_views import ChildRecordView
from wvi.views.kader_views import KaderView
from wvi.views.correspondence_views import CorrespondenceView
from wvi.views.participant_views import ParticipantView


urlpatterns = [
    path('', CustomAuthentication.loginView, name='login'),
    
    # Authentication
    path('login/', CustomAuthentication.loginView, name='login'),
    path('logout/', CustomAuthentication.logoutView, name='logout'),
    path('signup/', CustomAuthentication.signupView, name='signup'),

    # Child
    path("child", ChildView.view, name="child"),
    path("child/update", ChildView.update),

    # Child Record
    path("childrecord", ChildRecordView.view, name="childrecord"),
    path("childrecord/insert_excel", ChildRecordView.insert_excel),
    path("childrecord/update", ChildRecordView.update),
    path("childrecord/update_target", ChildRecordView.update_target),

    # Kader
    path("kader", KaderView.view, name="kader"),
    path("kader/insert", KaderView.insert),
    path("kader/update", KaderView.update),
    path("kader/delete", KaderView.delete),

    # Correspondence
    path("correspondence", CorrespondenceView.view, name="correspondence"),
    path("correspondence/insert_excel", CorrespondenceView.insert_excel),
    path("correspondence/update_kader", CorrespondenceView.update_kader),
    path("correspondence/update_due_date", CorrespondenceView.update_due_date),

    # Participant
    path("participant", ParticipantView.view, name="participant"),
    path("participant/insert_excel", ParticipantView.insert_excel, name="participant_insert_excel"),
]