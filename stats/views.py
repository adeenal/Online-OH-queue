from django.views import View
from users.models import StudentUser
from ohqueue.models import OHQueue
from questions.models import Question
from rest_framework import generics
from .utils import dateLastStartOfWeek
from rest_framework.permissions import IsAuthenticated
from questions.serializers import QuestionSerializer
from django.http import HttpResponse, JsonResponse
from api.permissions import TAPermission

import numpy as np
import pandas as pd
import pytz
import os
import datetime

class SummaryList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (TAPermission,)

    def get_queryset(self):
       # get all of the question
       last_date = dateLastStartOfWeek()
       questions = Question.objects.filter(ask_date__gte=last_date).order_by("host_queue")
       return questions

class FrequentUserView(View):
    def get(self, request,  *args, **kwargs):
        all_questions = Question.objects.all()

        token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
        if token_header == None or " " not in token_header:
            return JsonResponse({"authenticated": False})
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first()
        if user == None or not user.is_superuser:
            return JsonResponse({"authenticated": False})
        if (len(all_questions.values()) == 0):
            return JsonResponse({"authenticated": True, "value": []})
        df = pd.DataFrame(list(all_questions.values()))
        results2 = df.groupby(['author_email', 'author_first_name', 'author_last_name']).answered_by_email.count()
        response2 = results2.to_dict()
        actualresponse = []
        for key in response2:
            element = {}
            element['email'] = key[0]
            element['fname'] = key[1]
            element['lname'] = key[2]
            element['count'] = response2[key]
            actualresponse.append(element)
        return_dictionary = {}
        return_dictionary["value"] = actualresponse
        return_dictionary["authenticated"] = True
        return JsonResponse(return_dictionary)
      
class FrequentAnswerView(View):
    def get(self, request, *args, **kwargs):
        all_questions = Question.objects.all()

        token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
        if token_header == None or " " not in token_header:
            return JsonResponse({"authenticated": False})
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first()
        if user == None or not user.is_superuser:
            return JsonResponse({"authenticated": False})
        if (len(all_questions.values()) == 0):
            return JsonResponse({"authenticated": True, "value": []})
        df = pd.DataFrame(list(all_questions.values()))
        results = df.groupby(by='answered_by_email').answered_by_email.count()
        results2 = df.groupby(['answered_by_email', 'answerer_first_name', 'answerer_last_name']).answered_by_email.count()
        response = results.to_dict()
        response2 = results2.to_dict()
        actualresponse = []
        for key in response2:
            element = {}
            element['email'] = key[0]
            element['fname'] = key[1]
            element['lname'] = key[2]
            element['count'] = response2[key]
            actualresponse.append(element)
        return_dictionary = {}
        return_dictionary["value"] = actualresponse
        return_dictionary["authenticated"] = True
        return JsonResponse(return_dictionary)

class UserQuestionsView(View):
    def get(self, request, *args, **kwargs):
        user_email = (self.kwargs["email"])
        

        user_questions = Question.objects.filter(author_email=user_email)
        if len(user_questions.values()) == 0:
            return JsonResponse({})
        df = pd.DataFrame(list(user_questions.values()))
        df['daystr'] = df.ask_date.dt.strftime('%Y-%m-%d')
        results = df.groupby(by='daystr').daystr.count()
        response = results.to_dict()
        return JsonResponse(response)

class GetAllStudentsView(View):
    def get(self, request, *args, **kwargs):
        users = StudentUser.objects.all()
        students = []
        for student in users:
            students.append(student.email)
        return JsonResponse({'value': students})

class GetTrafficTimesView(View):
    def get(self, request, *args, **kwargs):
        all_questions = Question.objects.all()
        if (len(all_questions.values()) == 0):
            return JsonResponse({})
        df = pd.DataFrame(list(all_questions.values()))
        df['tznormal'] = df['ask_date'].apply(
            lambda x: x.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(os.environ.get('QUEUE_TIME_ZONE','America/New_York')))
        )

        ohqentries = OHQueue.objects.all()
        monday_slots = []
        tuesday_slots = []
        wednesday_slots = []
        thursday_slots = []
        friday_slots = []
        saturday_slots = []
        sunday_slots = []

        for queue in ohqentries:
            m_times = self.time_slots_to_hour_blocks(queue.monday_times)
            t_times = self.time_slots_to_hour_blocks(queue.tuesday_times)
            w_times = self.time_slots_to_hour_blocks(queue.wednesday_times)
            tr_times = self.time_slots_to_hour_blocks(queue.thursday_times)
            f_times = self.time_slots_to_hour_blocks(queue.friday_times)
            sat_times = self.time_slots_to_hour_blocks(queue.saturday_times)
            sun_times = self.time_slots_to_hour_blocks(queue.sunday_times)

            monday_slots += m_times
            tuesday_slots += t_times
            wednesday_slots += w_times
            thursday_slots += tr_times
            friday_slots += f_times
            saturday_slots += sat_times
            sunday_slots += sun_times
        
        monday_slots = list(set(monday_slots))
        tuesday_slots = list(set(tuesday_slots))
        wednesday_slots = list(set(wednesday_slots))
        thursday_slots = list(set(thursday_slots))
        friday_slots = list(set(friday_slots))
        saturday_slots = list(set(saturday_slots))
        sunday_slots = list(set(sunday_slots))

        df['slot'] = df.tznormal.apply(self.tz_to_slot)

        result = df.groupby(by='slot').slot.count()
        dictresult = result.to_dict()
        return JsonResponse(dictresult)
    
    def tz_to_slot(self, time):
        result = self.buckets_for_date(time)
        slotstr = ""
        if result[0] == 0:
            slotstr += "Mon "
        elif result[0] == 1:
            slotstr += "Tues "
        elif result[0] == 1:
            slotstr += "Wed "
        elif result[0] == 1:
            slotstr += "Thurs "
        elif result[0] == 1:
            slotstr += "Fri "
        elif result[0] == 1:
            slotstr += "Sat "
        elif result[0] == 1:
            slotstr += "Sun "
        
        slotstr += result[1]
        return slotstr
        
    def buckets_for_date(self, ask_date):
        day_week_number = ask_date.weekday()
        curr_hour_str = ask_date.strftime("%I:00%p")
        one_hour_str = (ask_date + datetime.timedelta(hours=1)).strftime("%I:00%p")
        time_interval = curr_hour_str + "-" + one_hour_str
        return day_week_number, time_interval

    def convert_timedelta_to_hours(self, duration):
            days, seconds = duration.days, duration.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = (seconds % 60)
            return hours

    def time_slots_to_hour_blocks(self, time_slot):
        hour_blocks = []
        all_intervals = []
        if time_slot == None or len(time_slot) == 0:
            return []
        if ";" in time_slot:
            all_intervals = time_slot.split(";")
        else:
            all_intervals = [time_slot]
        for interval in all_intervals:
            if "-" in interval:
                start_time = interval.split("-")[0]
                end_time = interval.split("-")[1]
                start_time_datetime = datetime.datetime.strptime(start_time, '%I:%M%p')
                end_time_datetime = datetime.datetime.strptime(end_time, '%I:%M%p')
                num_hours = self.convert_timedelta_to_hours(end_time_datetime - start_time_datetime)

                curr_time = start_time_datetime
                for i in range(num_hours):
                    next_hour = curr_time + datetime.timedelta(hours=1)
                    curr_time_str = curr_time.strftime("%I:%M%p")
                    next_hour_str = next_hour.strftime("%I:%M%p")
                    timeslot = curr_time_str + "-" + next_hour_str
                    hour_blocks.append(timeslot)
                    curr_time = next_hour
        return hour_blocks
