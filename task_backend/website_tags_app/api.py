
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import User
from .service import html_tag_searching, parcing_qs, difference_in_dicts, parcing_phone, random_6_chars

class Auth(viewsets.ViewSet):

    def list(self, request):
        qs = request.META["QUERY_STRING"]

        if ("phone" in qs):
            phone = parcing_phone(qs)
            if phone == None:
                return Response("Try phone number in format +01234567890",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Please add correct query string, ?phone=+01234567890",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_phone=phone)
            return Response(user.secret_code)
        except:
            rand_chars = random_6_chars()
            User.objects.create(user_phone=phone, secret_code=rand_chars)
            return Response(rand_chars)


    def create(self, request):
        input_data = request.data
        if "phone" not in input_data.keys():
            return Response("Is 'phone' in request?", status=status.HTTP_400_BAD_REQUEST)
        if "code" not in input_data.keys():
            return Response("Is 'code' in request?", status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.get(user_phone=input_data["phone"], secret_code=input_data["code"])
        except User.DoesNotExist:
            return Response({"status": "Fail"})
        return Response({"status": "OK"})


class WebSiteTags(viewsets.ViewSet):

    @method_decorator(cache_page(60*60)) # cache for one hour
    def list(self, request, link = "freestylo.ru"):

        tags = None

        #parcing query_string

        qs = request.META["QUERY_STRING"]
        if ("link" in qs or 'tags' in qs):
            link_qs, tags = parcing_qs(qs)
            if link_qs != None:
                link = link_qs

        #get tags dict
        tags_dict = html_tag_searching(link)

        #Validate response
        if tags_dict == None:
            return Response("Try another link or delete protocol part. Example ?link=example.com", status=status.HTTP_400_BAD_REQUEST)

        # Tags adding to response
        if tags == None:
            return Response(tags_dict)
        else:
            result = {}
            for tag in tags:
                try:
                    result[tag] = tags_dict.get(tag)
                except KeyError:
                    pass
            return Response(result)


class WebSiteCheck(viewsets.ViewSet):

    def create(self,  request):
        input_data = request.data
        #print(input_data)
        if "link" not in input_data.keys():
            return Response("Is 'link' in request?", status=status.HTTP_400_BAD_REQUEST)
        if "structure" not in input_data.keys():
            return Response("Is 'structure' in request?", status=status.HTTP_400_BAD_REQUEST)
        elif type(input_data["structure"]) != type({}):
            return Response("Is 'structure' value dictionary?", status=status.HTTP_400_BAD_REQUEST)
        tags_dict = html_tag_searching(input_data["link"])


        tags_dict = WebSiteTags.list(self, request=request, link=input_data["link"]).data


        if tags_dict == input_data["structure"]:
            return Response({"is_correct": True})
        else:
            result = difference_in_dicts(input_data["structure"], tags_dict)

            return Response(result)