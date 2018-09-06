#!/usr/bin/env python
"""
Entry Management Functionality
"""

import json
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

from entry_manager import EntryManager


class EntryRest(APIView):
    """
    Entry Rest API to get Entry and post Entry
    """
    __name__ = 'EntryRest'

    def __init__(self):
        pass

    def get(self, request):
        """
        List All Entrys.
        :param request: HttpRequest (Get) to retrieve all Entrys
        :return: HttpResponse with all Entry meta
        """
        print "in EntryRest get"
        response, status = dict(), None
        temp_obj = EntryManager()
        response = temp_obj.list_entry()
        return HttpResponse(json.dumps(response))

    def post(self, request):
        """
        Add a new Entry from JSON input
        :param request: HttpRequest (Post) to add a new Entry JSON
        :return: HttpResponse with successfully added message or
                 HttpResponseBadRequest for bad request or HttpResponseNotFound for invalid input
        """
        response, status = dict(), None
        print "in Entryrest post"
        try:
            Entry = json.loads(request.body)
        except ValueError as v_err:
            response['error'] = 'Invalid input JSON - %s' % str(v_err)
            return HttpResponseBadRequest(json.dumps(response))

        temp_obj = EntryManager()
        response, status = temp_obj.upload_new_entry(Entry)
        if status == 200:
            return HttpResponse(json.dumps(response))
        if status == 400:
            return HttpResponseBadRequest(json.dumps(response))


class EntryType(APIView):
    """
    Entry Status Rest
    """
    __name__ = 'EntryType'

    def get(self, request, entry_id):
        """
        Get Status of specified Entry id.
        :param request: HttpRequest (Get) to retrieve specific Entry status
        :param entry_id : Entry id to get status
        :return: HttpResponse with Entry status or HttpResponseBadRequest for bad request or
                 HttpResponseNotFound for invalid input
        """
        print "in Entry type get"
        response, status = dict(), None
        try:
            temp_obj = EntryManager()
            response, status = temp_obj.get_entry_type(entry_id)
            if status == 200:
                return HttpResponse(json.dumps(response))
            if status == 400:
                return HttpResponseBadRequest(json.dumps(response))
        except Exception as exception:
            response['error'] = 'Failed to retrieve record type'
            response["message"] = "Exception : %s " % (str(exception))
            return HttpResponseBadRequest(json.dumps(response))


class EntryOperations(APIView):
    """
    Entry Operations- Get/delete/update Entry rest
    """
    __name__ = 'EntryOperations'

    def get(self, request, entry_id):
        """
        Get Entry details of specified Entry id.
        :param request: HttpRequest (Get) to retrieve specific Entry JSON
        :param entry_id: Entry id to get Entry JSON
        :return: HttpResponse with Entry JSON or HttpResponseBadRequest for bad request or
                 HttpResponseNotFound for invalid input
        """
        # self.logger("API Call - Get Entry.")
        response, status = dict(), None
        print "in Temp oper get"
        try:
            temp_obj = EntryManager()
            response, status = temp_obj.get_entry(entry_id)
            if status == 200:
                return HttpResponse(json.dumps(response))
            if status == 404:
                return HttpResponseNotFound(json.dumps(response))
        except Exception as exception:
            response['error'] = 'Failed to retrieve record'
            response["message"] = "Exception : %s " % (str(exception))
            return HttpResponseBadRequest(json.dumps(response))

    def delete(self, request, entry_id):
        """
        Delete specified Entry id.
        :param request: HttpRequest (Get) to teardown specific Entry
        :param entry_id: Entry id to teardown
        :return: HttpResponse with successful teardown message or
                 HttpResponseBadRequest for bad request or HttpResponseNotFound for invalid input
        """
        # self.logger("API Call - Teardown Entry.")
        response, status = dict(), None
        print " in temp oper delete", entry_id
        try:
            temp_obj = EntryManager()
            response, status = temp_obj.remove_entry(entry_id)
            if status == 200:
                return HttpResponse(json.dumps(response))
            if status == 400:
                return HttpResponseBadRequest(json.dumps(response))
            if status == 404:
                return HttpResponseNotFound(json.dumps(response))
        except Exception as exception:
            response['error'] = 'Failed to delete record'
            response['message'] = "Exception : %s" % (str(exception))
            return HttpResponseBadRequest(json.dumps(response))

    def put(self, request, entry_id):
        """
        Update JSON details to specified Entry id.
        :param request: HttpRequest (Put) to update specific Entry
        :param entry_id: Entry id to update Entry
        :return: HttpResponse with successfully update message or
                 HttpResponseBadRequest for bad request or HttpResponseNotFound for invalid input
        """
        response, status = dict(), None
        print "in temp oper put "
        try:
            new_data = json.loads(request.body)
        except ValueError as v_err:
            response['error'] = 'Invalid input JSON - %s' % str(v_err)
            return HttpResponseBadRequest(json.dumps(response))

        try:
            temp_obj = EntryManager()
            response, status = temp_obj.update_entry(entry_id, new_data)
            if status == 200:
                return HttpResponse(json.dumps(response))
            if status == 400:
                return HttpResponseBadRequest(json.dumps(response))
            if status == 404:
                return HttpResponseNotFound(json.dumps(response))
        except Exception as exception:
            response['error'] = 'Failed to update record'
            response['message'] = "Exception : %s " % (str(exception))
            return HttpResponseBadRequest(json.dumps(response))
