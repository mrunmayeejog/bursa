#!/usr/bin/env python
"""
Entry Management Functionality
"""
import os
import datetime
from dateutil.relativedelta import *
from datetime import date
from rest_framework.views import APIView
from models import Entry

__name__ = 'EntryManager'


class EntryManager(APIView):
    """
    EntryManager - Manage Entry functionality
    """

    def __init__(self):
        pass

    @staticmethod
    def list_entry():
        """
        Method to list all Entrys
        :return: List of Entrys with meta information
        """

        # Read all Entrys from database
        all_entries = Entry.objects.all()
        response, temp = {}, []
        # Add all Entrys to response
        for x_temp in all_entries:
            temp.append({"record_id": x_temp.id, "type": x_temp.type,
                         "amount": x_temp.amount, "place": x_temp.place, "category" : x_temp.category,
                         "created_date": x_temp.date.isoformat()})
        return temp


    @staticmethod
    def upload_new_entry(entry_data):
        """
        Upload new Entry as JSON input
        :param entry_data: Upload Entry JSON as new Entry
        :return: Status and message for JSON upload operation
        """
        response = dict()
        entry_id = os.urandom(4).encode('hex')
        record = Entry()
        record.id = entry_id
        record.amount = entry_data.get('amount', '0.0')
        record.type = entry_data.get('type', 'C')
        record.place = entry_data.get('place', '')
        record.category = entry_data.get('category', '')
        record.save()
        response['status'] = 'Added new record'
        status = 200
        return response, status

    '''
    def is_available(self):
        """
        Check if Entry state is available
        :return: True if state is available else return false
        """
        x_temp = Entry.objects.filter(id=self.entry_id)
        if len(x_temp) == 0:
            log_handler.error(
                'Entry does not exist for id - %s.', self.entry_id)
            return False
        if x_temp[0].state == constant.AVAILABLE:
            return True
        return False
    '''

    def get_entry_type(self, entry_id):
        """
        Get Entry status
        :return: Return Entry status
        """
        response = dict()
        x_temp = Entry.objects.filter(id=entry_id)
        if len(x_temp) == 0:
            response['error'] = 'Invalid Entry Id.'
            status = 400
            return response, status
        response['type'] = x_temp[0].type
        response['entry_id'] = entry_id
        status = 200
        return response, status

    def get_entry(self, entry_id):
        """
        Get specific Entry details
        :return: Entry JSON for specific Entry
        """
        print "in get Entry"
        response = dict()
        x_temp = Entry.objects.filter(id=entry_id)
        print x_temp
        if len(x_temp) == 0:
            response['error'] = 'Invalid Entry Id.'
            status = 404
            return response, status

        response = {"record_id": x_temp[0].id, "type": x_temp[0].type,
                         "amount": x_temp[0].amount, "place": x_temp[0].place, "category" : x_temp[0].category,
                         "created_date": x_temp[0].date.isoformat()}
        status = 200
        return response, status

    def update_entry(self, entry_id, new_data):
        """
        Update specific Entry JSON
        :param new_data: Update new data for specified Entry
        :return: Status and message for Entry update operation
        """
        x_temp = Entry.objects.filter(id=entry_id)
        response = dict()
        if len(x_temp) == 0:
            response['error'] = 'Invalid Entry Id.'
            status = 404
            return response, status

        record = x_temp[0]
        record.amount = new_data.get('amount', x_temp[0].amount)
        record.type = new_data.get('type', x_temp[0].type)
        record.place = new_data.get('place', x_temp[0].place)
        record.category = new_data.get('category', x_temp[0].category)
        record.save()
        response['status'] = 'Record updated'
        status = 200
        return response, status

    def remove_entry(self, entry_id):
        """
        Remove specified Entry
        :return: Status and message for Entry removal operation
        """
        x_temp = Entry.objects.filter(id=entry_id)
        response = dict()
        print "in delete"
        if len(x_temp) == 0:
            response['error'] = 'Invalid Entry Id.'
            status = 404
            return response, status

        x_temp.delete()
        response['status'] = 'Entry removed'
        status = 200
        return response, status

    def get_expenses(self, sortby):
        """

        :param sortby:
        :return:
        """
        all_entries = Entry.objects.all().values('amount')
        response, temp = {}, []
        expenses = {}
        #for x_temp in all_entries:
        total = sum([i['amount'] for i in all_entries])
        print "$$$$$$$$$$$$$$", total
        today_ex = Entry.objects.filter(date__date=date.today()).values('amount')
        today_total = sum([i['amount'] for i in today_ex])
        print "today ", today_total

        pre_date = str(datetime.now() + relativedelta(months=-1))
        print "ghutyutru", pre_date
        last_month = Entry.objects.filter(date__gt=pre_date).values('amount')
        last_month_ex = sum([i['amount'] for i in last_month])
        print "last month ", last_month_ex
