from django.shortcuts import render, HttpResponse
from django.db import connection
import json 
from . import models
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
import io



class SearchBuses(APIView):
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        json_data = request.body 
        streamed = io.BytesIO(json_data)
        python_data = JSONParser().parse(streamed) 

        source = python_data.get("source", None)
        destination = python_data.get("destination", None)
        if not source or not destination:
            return HttpResponse(json.dumps({"error":"source and destination required"}),  content_type='application/json',status=400)
        buses = self.search_buses(source, destination)
        formatted_buses = [
            {
                'id': row[0],
                'name': row[1],
                'source': row[2],
                'destination': row[3],
                'date_of_journey': row[4].strftime('%Y-%m-%d %H:%M:%S')
            }
            for row in buses
        ]
        
        json_data = json.dumps({"buses":formatted_buses})
        print("search result", json_data, type(json_data))
        return HttpResponse(json_data, content_type='application/json',status=200)
        
    def search_buses(self, source, destination):
        with connection.cursor() as cursor:
            query = """
                SELECT DISTINCT b.id, b.name, b.source, b.destination, b.date_of_journey 
                FROM services_bus b
                JOIN services_bus_route sbr ON b.id = sbr.bus_id
                JOIN services_routes r ON sbr.routes_id = r.id
                WHERE r.route LIKE %s
                AND r.route LIKE %s
                AND POSITION(%s IN r.route) < POSITION(%s IN r.route);
            """
            cursor.execute(query, [f'%{source}%', f'%{destination}%', source, destination])
            result = cursor.fetchall()
            
        return result
    
class Block(APIView):
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)

        no_passengers = python_data.get("no_passengers", None)
        bus_name = python_data.get("bus_name", None)
        if not no_passengers or not bus_name:
            return HttpResponse(json.dumps({"error":"number of passengers required"}),  content_type='application/json',status=400)
        # Retrieve the bus instance by name
        bus = get_object_or_404(models.Bus, name=bus_name)
        # Retrieve the seats instance related to this bus
        seats = get_object_or_404(models.Seats, bus=bus)

        # Create the Block object
        
        block_obj = models.Block.objects.create(seats_bus=seats, blocked_seats=no_passengers)
        blockID = str(block_obj.block_id )
        json_data = json.dumps({"block_id":blockID})
        return HttpResponse(json_data, content_type='application/json', status = 200)
    
class BookBus(APIView):
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        block_id = python_data.get("block_id", None)
        if not block_id:
             return HttpResponse(json.dumps({"error":"block id  required"}),  content_type='application/json',status=400)
        block_obj = models.Block.objects.get(block_id = block_id)
        block_obj_seats_bus = block_obj.seats_bus
        block_obj_blocked_seats =  block_obj.blocked_seats
        block_obj.delete()
        book_obj = models.Book.objects.create(seats_bus = block_obj_seats_bus, booked_seats = block_obj_blocked_seats)
        book_obj_id = str(book_obj.book_id)
        json_data = json.dumps({"book_id":book_obj_id})
        return HttpResponse(json_data, content_type='application/json', status = 200)




    

            

