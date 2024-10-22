import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import matplotlib.pyplot as plt
import io
import sqlite3
from datetime import datetime, timedelta
import random

fake = Faker()

# Add this at the beginning of the file, after the imports and before the custom generators

DOMAIN_SCHEMAS = {
    "E-commerce Customer Data": {
        "customer_id": int,
        "name": str,
        "email": str,
        "age": int,
        "purchase_amount": float,
        "last_purchase_date": "datetime",
        "loyalty_points": int,
        "preferred_category": str
    },
    "Healthcare Patient Records": {
        "patient_id": int,
        "name": str,
        "date_of_birth": "datetime",
        "blood_type": str,
        "weight_kg": float,
        "height_cm": int,
        "last_visit": "datetime",
        "insurance_number": str
    },
    "Financial Transactions": {
        "transaction_id": int,
        "account_number": str,
        "transaction_date": "datetime",
        "amount": float,
        "transaction_type": str,
        "merchant_name": str,
        "category": str
    },
    "HR Employee Data": {
        "employee_id": int,
        "full_name": str,
        "department": str,
        "salary": float,
        "hire_date": "datetime",
        "performance_score": float,
        "manager_id": int
    },
    "Restaurant Orders": {
        "order_id": int,
        "customer_name": str,
        "order_time": "datetime",
        "total_amount": float,
        "items_ordered": int,
        "table_number": int,
        "tip_amount": float
    },
    "Real Estate Listings": {
        "property_id": int,
        "address": str,
        "price": float,
        "square_feet": int,
        "bedrooms": int,
        "bathrooms": float,
        "year_built": int,
        "listing_date": "datetime"
    },
    "Educational Student Records": {
        "student_id": int,
        "name": str,
        "gpa": float,
        "major": str,
        "enrollment_date": "datetime",
        "credits_completed": int,
        "graduation_year": int
    },
    "Inventory Management": {
        "product_id": int,
        "product_name": str,
        "quantity": int,
        "unit_price": float,
        "reorder_level": int,
        "last_restocked": "datetime",
        "supplier_id": int
    },
    "Social Media Posts": {
        "post_id": int,
        "user_handle": str,
        "post_date": "datetime",
        "likes": int,
        "shares": int,
        "comment_count": int,
        "content_type": str
    },
    "Weather Data": {
        "station_id": int,
        "timestamp": "datetime",
        "temperature": float,
        "humidity": float,
        "precipitation": float,
        "wind_speed": float,
        "pressure": float
    },
    "Fitness Tracking": {
        "workout_id": int,
        "user_id": int,
        "workout_date": "datetime",
        "duration_minutes": int,
        "calories_burned": float,
        "heart_rate": int,
        "workout_type": str
    },
    "Library Records": {
        "book_id": int,
        "title": str,
        "author": str,
        "isbn": str,
        "checkout_date": "datetime",
        "due_date": "datetime",
        "member_id": int
    },
    "Travel Bookings": {
        "booking_id": int,
        "passenger_name": str,
        "destination": str,
        "departure_date": "datetime",
        "return_date": "datetime",
        "ticket_price": float,
        "booking_status": str
    },
    "Vehicle Fleet Management": {
        "vehicle_id": int,
        "model": str,
        "year": int,
        "mileage": float,
        "last_service": "datetime",
        "fuel_efficiency": float,
        "status": str
    },
    "Event Registration": {
        "registration_id": int,
        "attendee_name": str,
        "event_date": "datetime",
        "ticket_type": str,
        "payment_amount": float,
        "registration_date": "datetime",
        "seat_number": str
    },
    "Supply Chain": {
        "shipment_id": int,
        "origin": str,
        "destination": str,
        "dispatch_date": "datetime",
        "arrival_date": "datetime",
        "weight_kg": float,
        "shipping_cost": float
    },
    "Marketing Campaign": {
        "campaign_id": int,
        "campaign_name": str,
        "start_date": "datetime",
        "end_date": "datetime",
        "budget": float,
        "leads_generated": int,
        "conversion_rate": float
    },
    "IT Support Tickets": {
        "ticket_id": int,
        "requester_name": str,
        "creation_date": "datetime",
        "priority": int,
        "status": str,
        "resolution_time": float,
        "category": str
    },
    "Hotel Reservations": {
        "reservation_id": int,
        "guest_name": str,
        "check_in": "datetime",
        "check_out": "datetime",
        "room_type": str,
        "room_rate": float,
        "num_guests": int
    },
    "Project Management": {
        "task_id": int,
        "task_name": str,
        "assigned_to": str,
        "start_date": "datetime",
        "due_date": "datetime",
        "completion_percentage": float,
        "priority": int
    },
    "Rental Equipment": {
        "rental_id": int,
        "equipment_name": str,
        "rental_date": "datetime",
        "return_date": "datetime",
        "daily_rate": float,
        "customer_id": int,
        "condition_status": str
    },
    "Insurance Claims": {
        "claim_id": int,
        "policy_number": str,
        "claim_date": "datetime",
        "claim_amount": float,
        "claim_type": str,
        "status": str,
        "adjuster_id": int
    },
    "Subscription Services": {
        "subscription_id": int,
        "user_email": str,
        "plan_type": str,
        "start_date": "datetime",
        "next_billing_date": "datetime",
        "monthly_cost": float,
        "status": str
    },
    "Warehouse Management": {
        "storage_id": int,
        "item_name": str,
        "quantity": int,
        "location_code": str,
        "last_counted": "datetime",
        "min_threshold": int,
        "storage_temp": float
    },
    "Gym Membership": {
        "member_id": int,
        "name": str,
        "join_date": "datetime",
        "membership_type": str,
        "monthly_fee": float,
        "last_visit": "datetime",
        "trainer_id": int
    },
    "Delivery Service": {
        "delivery_id": int,
        "customer_name": str,
        "delivery_address": str,
        "order_time": "datetime",
        "delivery_time": "datetime",
        "package_weight": float,
        "delivery_status": str
    },
    "Parking Management": {
        "parking_id": int,
        "vehicle_plate": str,
        "entry_time": "datetime",
        "exit_time": "datetime",
        "parking_spot": str,
        "fee": float,
        "vehicle_type": str
    },
    "Conference Registration": {
        "registration_id": int,
        "attendee_name": str,
        "conference_date": "datetime",
        "ticket_type": str,
        "payment_status": str,
        "dietary_preferences": str,
        "session_tracks": str
    },
    "Mobile App Analytics": {
        "session_id": int,
        "user_id": str,
        "session_start": "datetime",
        "session_duration": float,
        "app_version": str,
        "device_type": str,
        "crash_count": int
    },
    "Utility Consumption": {
        "meter_id": int,
        "reading_date": "datetime",
        "consumption": float,
        "peak_usage": float,
        "utility_type": str,
        "building_id": int,
        "cost": float
    }
}

# Custom generators for specific fields
def generate_blood_type():
    return random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])

def generate_department():
    return random.choice(['HR', 'IT', 'Finance', 'Marketing', 'Sales', 'Operations', 'R&D', 'Legal'])

def generate_transaction_type():
    return random.choice(['PURCHASE', 'REFUND', 'TRANSFER', 'WITHDRAWAL', 'DEPOSIT'])

def generate_course_major():
    return random.choice(['Computer Science', 'Business', 'Engineering', 'Medicine', 'Law', 'Arts', 'Physics', 'Mathematics'])

def generate_product_category():
    return random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home', 'Sports', 'Beauty', 'Toys'])

def generate_subscription_plan():
    return random.choice(['Basic', 'Premium', 'Enterprise', 'Free Trial', 'Student', 'Family'])

def generate_weather_condition():
    return random.choice(['Sunny', 'Cloudy', 'Rainy', 'Stormy', 'Partly Cloudy', 'Clear', 'Foggy', 'Snowy'])

def generate_workout_type():
    return random.choice(['Cardio', 'Strength', 'HIIT', 'Yoga', 'Swimming', 'Running', 'Cycling', 'CrossFit'])

def generate_book_genre():
    return random.choice(['Fiction', 'Non-Fiction', 'Mystery', 'Science Fiction', 'Romance', 'Biography', 'History', 'Technical'])

def generate_vehicle_status():
    return random.choice(['Available', 'In Use', 'Maintenance', 'Repair', 'Out of Service'])

def generate_ticket_type():
    return random.choice(['VIP', 'Regular', 'Early Bird', 'Student', 'Group', 'Senior'])

def generate_shipping_status():
    return random.choice(['Processing', 'Shipped', 'In Transit', 'Delivered', 'Delayed', 'Returned'])

def generate_project_status():
    return random.choice(['Not Started', 'In Progress', 'On Hold', 'Completed', 'Cancelled'])

def generate_room_type():
    return random.choice(['Single', 'Double', 'Suite', 'Deluxe', 'Executive', 'Family'])

def generate_priority_level():
    return random.choice(['Low', 'Medium', 'High', 'Critical', 'Urgent'])

# Domain-specific value generators
class DomainValueGenerator:
    @staticmethod
    def e_commerce(field):
        if field == "customer_id":
            return fake.random_int(min=10000, max=99999)
        elif field == "email":
            return fake.email()
        elif field == "purchase_amount":
            return round(random.uniform(10, 1000), 2)
        elif field == "loyalty_points":
            return random.randint(0, 10000)
        elif field == "preferred_category":
            return generate_product_category()
        return None

    @staticmethod
    def healthcare(field):
        if field == "patient_id":
            return fake.random_int(min=100000, max=999999)
        elif field == "blood_type":
            return generate_blood_type()
        elif field == "weight_kg":
            return round(random.uniform(40, 120), 1)
        elif field == "height_cm":
            return random.randint(150, 200)
        elif field == "insurance_number":
            return fake.uuid4()[:8].upper()
        return None

    @staticmethod
    def financial(field):
        if field == "transaction_id":
            return fake.random_int(min=1000000, max=9999999)
        elif field == "account_number":
            return fake.bban()
        elif field == "amount":
            return round(random.uniform(1, 10000), 2)
        elif field == "transaction_type":
            return generate_transaction_type()
        elif field == "merchant_name":
            return fake.company()
        return None

    @staticmethod
    def hr(field):
        if field == "employee_id":
            return fake.random_int(min=1000, max=9999)
        elif field == "department":
            return generate_department()
        elif field == "salary":
            return round(random.uniform(30000, 150000), 2)
        elif field == "performance_score":
            return round(random.uniform(1, 5), 1)
        return None

    @staticmethod
    def restaurant(field):
        if field == "order_id":
            return fake.random_int(min=1000, max=9999)
        elif field == "table_number":
            return random.randint(1, 50)
        elif field == "items_ordered":
            return random.randint(1, 10)
        elif field == "total_amount":
            return round(random.uniform(10, 200), 2)
        elif field == "tip_amount":
            return round(random.uniform(2, 40), 2)
        return None

    @staticmethod
    def real_estate(field):
        if field == "property_id":
            return fake.random_int(min=100000, max=999999)
        elif field == "price":
            return round(random.uniform(100000, 1000000), 2)
        elif field == "square_feet":
            return random.randint(500, 5000)
        elif field == "bedrooms":
            return random.randint(1, 6)
        elif field == "bathrooms":
            return round(random.uniform(1, 4), 1)
        elif field == "year_built":
            return random.randint(1960, 2023)
        return None

# Add more domain-specific generators here...

# Enhanced generate_fake_value function with domain-specific logic
def generate_fake_value(field, dtype, domain):
    # First check for domain-specific generators
    domain_generators = {
        "E-commerce Customer Data": DomainValueGenerator.e_commerce,
        "Healthcare Patient Records": DomainValueGenerator.healthcare,
        "Financial Transactions": DomainValueGenerator.financial,
        "HR Employee Data": DomainValueGenerator.hr,
        "Restaurant Orders": DomainValueGenerator.restaurant,
        "Real Estate Listings": DomainValueGenerator.real_estate
        # Add more domain mappings here...
    }

    if domain in domain_generators:
        value = domain_generators[domain](field)
        if value is not None:
            return value

    # Default generators for common fields
    if "date" in field.lower() or "time" in field.lower() or dtype == "datetime":
        if "birth" in field.lower():
            return fake.date_of_birth(minimum_age=18, maximum_age=90)
        else:
            return fake.date_time_between(start_date='-1y', end_date='now')
    
    if dtype == str:
        if "name" in field.lower():
            return fake.name()
        elif "email" in field.lower():
            return fake.email()
        elif "address" in field.lower():
            return fake.address()
        elif "phone" in field.lower():
            return fake.phone_number()
        elif "company" in field.lower() or "merchant" in field.lower():
            return fake.company()
        elif "status" in field.lower():
            return random.choice(['Active', 'Pending', 'Completed', 'Cancelled'])
        else:
            return fake.word()
    
    elif dtype == int:
        if "age" in field.lower():
            return random.randint(18, 90)
        elif "quantity" in field.lower():
            return random.randint(1, 100)
        elif "count" in field.lower():
            return random.randint(0, 1000)
        elif "id" in field.lower():
            return fake.random_int(min=10000, max=99999)
        else:
            return fake.random_int(min=0, max=10000)
    
    elif dtype == float:
        if "amount" in field.lower() or "price" in field.lower():
            return round(random.uniform(10, 1000), 2)
        elif "rate" in field.lower():
            return round(random.uniform(0, 1), 3)
        else:
            return round(random.uniform(0, 100), 2)

    return None

# Function to generate fake data
def generate_fake_data(schema, num_records, data_quality, domain):
    data = {}
    for column, dtype in schema.items():
        data[column] = [generate_fake_value(column, dtype, domain) for _ in range(num_records)]
    
    df = pd.DataFrame(data)
    
    # Introduce noise based on data quality
    if data_quality < 1:
        noise_factor = 1 - data_quality
        for column in df.select_dtypes(include=[np.number]).columns:
            mask = np.random.random(len(df)) < noise_factor
            df.loc[mask, column] = np.nan
    
    return df

# Main Streamlit app
def main():
    st.title("🎲 Fake Data Generator")
    st.write("Generate realistic fake datasets for various business domains!")

    # Domain selection
    selected_domain = st.selectbox(
        "Select a domain for your dataset:",
        list(DOMAIN_SCHEMAS.keys())
    )

    # Show selected schema
    st.subheader("Schema for Selected Domain")
    st.write(DOMAIN_SCHEMAS[selected_domain])

    # Dataset size
    num_records = st.slider("Number of records", 100, 10000, 1000)

    # Data quality control
    data_quality = st.slider("Data Quality (0: Very Dirty, 1: Clean)", 0.0, 1.0, 0.9, 0.1)

    # Generate data
    if st.button("Generate Data"):
        with st.spinner("Generating fake data..."):
            df = generate_fake_data(DOMAIN_SCHEMAS[selected_domain], num_records, data_quality, selected_domain)
            
            st.subheader("Preview of Generated Data")
            st.write(df.head())

            # Data export options
            st.subheader("Export Data")
            export_format = st.radio("Select export format", ["CSV"])
            
            if export_format == "CSV":
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "fake_data.csv", "text/csv")


            # Data profiling
            st.subheader("Data Profiling")
            st.write(df.describe())
            st.write("Missing Values Count:")
            st.write(df.isnull().sum())

if __name__ == "__main__":
    main()