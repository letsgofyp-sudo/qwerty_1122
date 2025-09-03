from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta, time
from decimal import Decimal
import json
from .models import UsersData, Vehicle, Trip, Route, RouteStop, TripStopBreakdown, Booking

@csrf_exempt
def get_ride_booking_details(request, trip_id):
    """Get complete ride details for passenger booking view"""
    if request.method == 'GET':
        try:
            # Get the trip with all related data
            trip = Trip.objects.select_related(
                'route', 'vehicle', 'driver'
            ).prefetch_related(
                'route__route_stops',
                'trip_bookings__passenger'
            ).get(trip_id=trip_id)
            
            # Debug logging
            print(f"Trip found: {trip.trip_id}")
            print(f"Route: {trip.route}")
            print(f"Vehicle: {trip.vehicle}")
            print(f"Driver: {trip.driver}")
            
            # Get route stops in order
            try:
                route_stops = trip.route.route_stops.all().order_by('stop_order')
                print(f"Route stops found: {route_stops.count()}")
            except Exception as e:
                print(f"Error getting route stops: {e}")
                route_stops = []
            
            # Get existing bookings for this trip
            try:
                existing_bookings = trip.trip_bookings.filter(booking_status='CONFIRMED').select_related('passenger')
                print(f"Existing bookings found: {existing_bookings.count()}")
            except Exception as e:
                print(f"Error getting bookings: {e}")
                existing_bookings = []
            
            # Calculate available seats
            available_seats = trip.available_seats
            
            # Get driver information
            try:
                driver_data = {
                    'id': trip.driver.id,
                    'name': trip.driver.name,
                    'driver_rating': float(trip.driver.driver_rating) if trip.driver.driver_rating else 0.0,
                    'profile_photo': f"/lets_go/user_image/{trip.driver.id}/profile_photo/" if trip.driver.profile_photo else None,
                    'phone_no': str(trip.driver.phone_no) if trip.driver.phone_no else None,
                    'gender': str(trip.driver.gender) if trip.driver.gender else None,
                }
                print(f"Driver data extracted: {driver_data['name']}")
            except Exception as e:
                print(f"Error extracting driver data: {e}")
                driver_data = {
                    'id': None,
                    'name': 'Unknown Driver',
                    'driver_rating': 0.0,
                    'profile_photo': None,
                    'phone_no': None,
                    'gender': 'Unknown',
                }
            
            # Get vehicle information
            try:
                vehicle_data = {
                    'id': trip.vehicle.id if trip.vehicle else None,
                    'model': str(trip.vehicle.model_number) if trip.vehicle and trip.vehicle.model_number else 'N/A',
                    'company': str(trip.vehicle.company_name) if trip.vehicle and trip.vehicle.company_name else 'N/A',
                    'type': str(trip.vehicle.vehicle_type) if trip.vehicle and trip.vehicle.vehicle_type else 'N/A',
                    'color': str(trip.vehicle.color) if trip.vehicle and trip.vehicle.color else 'N/A',
                    'seats': int(trip.vehicle.seats) if trip.vehicle and trip.vehicle.seats else 0,
                    'photo_front': f"/lets_go/vehicle_image/{trip.vehicle.id}/photo_front/" if trip.vehicle and trip.vehicle.photo_front else None,
                }
                print(f"Vehicle data extracted: {vehicle_data['model']}")
            except Exception as e:
                print(f"Error extracting vehicle data: {e}")
                vehicle_data = {
                    'id': None,
                    'model': 'N/A',
                    'company': 'N/A',
                    'type': 'N/A',
                    'color': 'N/A',
                    'seats': 0,
                    'photo_front': None,
                }
            
            # Get route information
            try:
                route_data = {
                    'id': str(trip.route.route_id) if trip.route.route_id else 'Unknown',
                    'name': str(trip.route.route_name) if trip.route.route_name else 'Custom Route',
                    'description': str(trip.route.route_description) if trip.route.route_description else 'Route description not available',
                    'total_distance_km': float(trip.route.total_distance_km) if trip.route.total_distance_km else 0.0,
                    'estimated_duration_minutes': int(trip.route.estimated_duration_minutes) if trip.route.estimated_duration_minutes else 0,
                    'stops': []
                }
                print(f"Route data extracted: {route_data['name']}")
            except Exception as e:
                print(f"Error extracting route data: {e}")
                route_data = {
                    'id': 'Unknown',
                    'name': 'Custom Route',
                    'description': 'Route description not available',
                    'total_distance_km': 0.0,
                    'estimated_duration_minutes': 0,
                    'stops': []
                }
            
            # Add route stops with coordinates
            try:
                for stop in route_stops:
                    route_data['stops'].append({
                        'order': int(stop.stop_order) if stop.stop_order else 0,
                        'name': str(stop.stop_name) if stop.stop_name else 'Unknown Stop',
                        'latitude': float(stop.latitude) if stop.latitude else 0.0,
                        'longitude': float(stop.longitude) if stop.longitude else 0.0,
                        'address': str(stop.address) if stop.address else 'No address',
                        'estimated_time_from_start': int(stop.estimated_time_from_start) if stop.estimated_time_from_start else 0,
                    })
                print(f"Added {len(route_data['stops'])} route stops")
            except Exception as e:
                print(f"Error processing route stops: {e}")
                # Add default stops if there's an error
                if len(route_data['stops']) == 0:
                    route_data['stops'] = [
                        {'order': 1, 'name': 'Start', 'latitude': 0.0, 'longitude': 0.0, 'address': 'Start location', 'estimated_time_from_start': 0},
                        {'order': 2, 'name': 'End', 'latitude': 0.0, 'longitude': 0.0, 'address': 'End location', 'estimated_time_from_start': 60}
                    ]
            
            # Get existing passengers information (for privacy, only show basic info)
            passengers_data = []
            try:
                for booking in existing_bookings:
                    if booking.passenger and booking.booking_status == 'CONFIRMED':
                        passengers_data.append({
                            'name': str(booking.passenger.name) if booking.passenger.name else 'Unknown',
                            'gender': str(booking.passenger.gender) if booking.passenger.gender else 'Unknown',
                            'passenger_rating': float(booking.passenger.passenger_rating) if booking.passenger.passenger_rating else 0.0,
                            'seats_booked': int(booking.number_of_seats) if booking.number_of_seats else 0,
                        })
                print(f"Added {len(passengers_data)} passenger records")
            except Exception as e:
                print(f"Error processing passenger data: {e}")
                passengers_data = []
            
            # Get fare calculation if available
            fare_data = {}
            try:
                if trip.fare_calculation:
                    # Ensure fare_calculation is a dict, not bytes
                    if isinstance(trip.fare_calculation, dict):
                        fare_data = trip.fare_calculation
                        # Always ensure base_fare matches the trip's base_fare (custom price)
                        fare_data['base_fare'] = float(trip.base_fare)
                        print(f"DEBUG: Using fare_calculation with corrected base_fare: {fare_data['base_fare']}")
                    else:
                        # If it's bytes or other type, create basic fare data
                        fare_data = {
                            'base_fare': float(trip.base_fare) if trip.base_fare else 0.0,
                            'total_distance_km': 0.0,
                            'price_per_km': 22.0,
                        }
                elif trip.route.total_distance_km:
                    # Calculate basic fare if no detailed calculation
                    base_fare_per_km = 22.0  # Default petrol rate
                    fare_data = {
                        'base_fare': float(trip.base_fare),
                        'total_distance_km': float(trip.route.total_distance_km),
                        'price_per_km': base_fare_per_km,
                    }
                print(f"Fare data extracted: {len(fare_data)} fields")
            except Exception as e:
                print(f"Error extracting fare data: {e}")
                fare_data = {
                    'base_fare': float(trip.base_fare) if trip.base_fare else 0.0,
                    'total_distance_km': 0.0,
                    'price_per_km': 22.0,
                }
            
            # Get stop breakdown if available
            stop_breakdown = []
            try:
                if hasattr(trip, 'stop_breakdowns') and trip.stop_breakdowns.exists():
                    breakdowns = trip.stop_breakdowns.all().order_by('from_stop_order')
                    for breakdown in breakdowns:
                        stop_breakdown.append({
                            'from_stop_order': int(breakdown.from_stop_order) if breakdown.from_stop_order else 0,
                            'to_stop_order': int(breakdown.to_stop_order) if breakdown.to_stop_order else 0,
                            'from_stop_name': str(breakdown.from_stop_name) if breakdown.from_stop_name else 'Unknown',
                            'to_stop_name': str(breakdown.to_stop_name) if breakdown.to_stop_name else 'Unknown',
                            'distance_km': float(breakdown.distance_km) if breakdown.distance_km else 0.0,
                            'duration_minutes': int(breakdown.duration_minutes) if breakdown.duration_minutes else 0,
                            'price': float(breakdown.price) if breakdown.price else 0.0,
                        })
                    print(f"Added {len(stop_breakdown)} stop breakdowns")
            except Exception as e:
                print(f"Error processing stop breakdowns: {e}")
                stop_breakdown = []
            
            # Prepare response data
            try:
                print(f"DEBUG: Trip base_fare from database: {trip.base_fare}")
                print(f"DEBUG: Trip fare_calculation: {trip.fare_calculation}")
                print(f"DEBUG: Trip base_fare type: {type(trip.base_fare)}")
                
                base_fare_float = float(trip.base_fare)
                print(f"DEBUG: Converted base_fare to float: {base_fare_float}")
                
                response_data = {
                    'success': True,
                    'trip': {
                        'trip_id': trip.trip_id,
                        'trip_date': trip.trip_date.isoformat(),
                        'departure_time': trip.departure_time.strftime('%H:%M'),
                        'estimated_arrival_time': trip.estimated_arrival_time.strftime('%H:%M') if trip.estimated_arrival_time else None,
                        'trip_status': trip.trip_status,
                        'total_seats': trip.total_seats,
                        'available_seats': available_seats,
                        'base_fare': base_fare_float,
                        'gender_preference': trip.gender_preference,
                        'notes': trip.notes,
                        'is_negotiable': trip.is_negotiable,
                        'minimum_acceptable_fare': float(trip.minimum_acceptable_fare) if trip.minimum_acceptable_fare else None,
                        'created_at': trip.created_at.isoformat(),
                    },
                    'driver': driver_data,
                    'vehicle': vehicle_data,
                    'route': route_data,
                    'passengers': passengers_data,
                    'fare_data': fare_data,
                    'stop_breakdown': stop_breakdown,
                    'booking_info': {
                        'can_book': available_seats > 0 and trip.trip_status == 'SCHEDULED',
                        'min_seats': 1,
                        'max_seats': min(available_seats, 4),  # Limit to 4 seats per booking
                        'price_per_seat': base_fare_float,
                        'total_price': base_fare_float,
                    }
                }
                print("Response data prepared successfully")
                print(f"Final response keys: {list(response_data.keys())}")
                print(f"DEBUG: Final trip data being sent to frontend:")
                print(f"  - base_fare: {response_data['trip']['base_fare']}")
                print(f"  - is_negotiable: {response_data['trip']['is_negotiable']}")
                print(f"  - booking_info.price_per_seat: {response_data['booking_info']['price_per_seat']}")
                return JsonResponse(response_data)
            except Exception as e:
                print(f"Error preparing response data: {e}")
                # Return a minimal response if there's an error
                return JsonResponse({
                    'success': True,
                    'trip': {
                        'trip_id': trip.trip_id,
                        'trip_date': trip.trip_date.isoformat() if trip.trip_date else None,
                        'departure_time': trip.departure_time.strftime('%H:%M') if trip.departure_time else 'N/A',
                        'trip_status': trip.trip_status,
                        'total_seats': trip.total_seats,
                        'available_seats': available_seats,
                        'base_fare': float(trip.base_fare) if trip.base_fare else 0.0,
                        'gender_preference': trip.gender_preference,
                        'notes': trip.notes,
                        'is_negotiable': trip.is_negotiable,
                        'minimum_acceptable_fare': float(trip.minimum_acceptable_fare) if trip.minimum_acceptable_fare else None,
                        'created_at': trip.created_at.isoformat() if trip.created_at else None,
                    },
                    'driver': driver_data,
                    'vehicle': vehicle_data,
                    'route': route_data,
                    'passengers': passengers_data,
                    'fare_data': fare_data,
                    'stop_breakdown': stop_breakdown,
                    'booking_info': {
                        'can_book': available_seats > 0 and trip.trip_status == 'SCHEDULED',
                        'min_seats': 1,
                        'max_seats': min(available_seats, 4),
                        'price_per_seat': float(trip.base_fare) if trip.base_fare else 0.0,
                        'total_price': float(trip.base_fare) if trip.base_fare else 0.0,
                    }
                })
            
        except Trip.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Trip not found'
            }, status=404)
        except Exception as e:
            print(f"Final exception caught: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': f'Error fetching trip details: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)

@csrf_exempt
def request_ride_booking(request, trip_id):
    """Request a ride booking"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            # Extract booking data
            passenger_id = data.get('passenger_id')
            from_stop_order = data.get('from_stop_order')
            to_stop_order = data.get('to_stop_order')
            number_of_seats = data.get('number_of_seats', 1)
            special_requests = data.get('special_requests', '')
            
            if not all([passenger_id, from_stop_order, to_stop_order, number_of_seats]):
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required fields: passenger_id, from_stop_order, to_stop_order, number_of_seats'
                }, status=400)
            
            # Get the trip
            trip = Trip.objects.get(trip_id=trip_id)
            
            # Check if trip is bookable
            if trip.trip_status != 'SCHEDULED':
                return JsonResponse({
                    'success': False,
                    'error': 'Trip is not available for booking'
                }, status=400)
            
            # Check seat availability
            if trip.available_seats < number_of_seats:
                return JsonResponse({
                    'success': False,
                    'error': f'Only {trip.available_seats} seats available'
                }, status=400)
            
            # Get passenger
            passenger = UsersData.objects.get(id=passenger_id)
            
            # Check if passenger already has a booking for this trip
            existing_booking = Booking.objects.filter(
                trip=trip,
                passenger=passenger,
                booking_status__in=['CONFIRMED']
            ).first()
            
            if existing_booking:
                return JsonResponse({
                    'success': False,
                    'error': 'You already have a booking for this trip'
                }, status=400)
            
            # Create the booking
            booking = Booking.objects.create(
                trip=trip,
                passenger=passenger,
                from_stop=trip.route.route_stops.get(stop_order=from_stop_order),
                to_stop=trip.route.route_stops.get(stop_order=to_stop_order),
                number_of_seats=number_of_seats,
                total_fare=trip.base_fare * number_of_seats,
                booking_status='CONFIRMED',  # Use the correct field name
                payment_status='PENDING'
            )
            
            # Update available seats
            trip.available_seats -= number_of_seats
            trip.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Ride booking requested successfully',
                'booking_id': booking.id,
                'status': booking.booking_status,
                'total_fare': float(booking.total_fare)
            })
            
        except Trip.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Trip not found'
            }, status=404)
        except UsersData.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Passenger not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error creating booking: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    }, status=405) 
