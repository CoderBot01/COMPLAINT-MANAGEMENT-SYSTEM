import ibm_db
from os import getenv
from dotenv import load_dotenv
import ibm_boto3
import string
import random
from constants import *
from ibm_botocore.client import Config

load_dotenv()

DB_URL = getenv("DB_URL")


class Functions:
    def __init__(self):
        self.conn = ibm_db.connect(
            DB_URL, '', '')
        self.create_tables()
        self.cos = self.setup_s3()

    def create_tables(self):
        try:
            ibm_db.exec_immediate(self.conn, "CREATE TABLE IF NOT EXISTS admins (id INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY, name VARCHAR(50), email VARCHAR(50) NOT NULL UNIQUE, password VARCHAR(200));")
            ibm_db.exec_immediate(self.conn, "CREATE TABLE IF NOT EXISTS users (id INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY, name VARCHAR(50), email VARCHAR(50) NOT NULL UNIQUE, password VARCHAR(200), phone VARCHAR(100));")
            ibm_db.exec_immediate(self.conn, "CREATE TABLE IF NOT EXISTS agents (id INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY, name VARCHAR(50), email VARCHAR(50) NOT NULL UNIQUE, password VARCHAR(200), role VARCHAR(100));")
            ibm_db.exec_immediate(self.conn, "CREATE TABLE IF NOT EXISTS complaints (email VARCHAR(50) NOT NULL, image_url VARCHAR(400), title VARCHAR(100), description VARCHAR(100), location_details VARCHAR(100), latitute VARCHAR(20), longitute VARCHAR(20), image_after VARCHAR(400), progress VARCHAR(20), assignee VARCHAR(100), ticket_id VARCHAR(100) NOT NULL UNIQUE, status VARCHAR(100), FOREIGN KEY (email) REFERENCES users(email));")
        except Exception as e:
            print(e)
        print("Connected to DB And  Created Tables")

    def add_newuser(self, name: str, mail: str, password: str, phone: str) -> bool:
        try:
            ibm_db.exec_immediate(
                self.conn, f"INSERT INTO users (name, email, password, phone) VALUES ('{name}', '{mail}', '{password}', '{phone}')")
            return True
        except Exception as e:
            print(e)
            return False

    def check_user(self, mail: str, password: str) -> bool:
        stmt = ibm_db.exec_immediate(
            self.conn, f"SELECT * FROM users WHERE EMAIL = '{mail}' AND PASSWORD = '{password}'")
        return ibm_db.fetch_row(stmt)

    def check_user_exists(self, mail: str) -> bool:
        stmt = ibm_db.exec_immediate(
            self.conn, f"SELECT * FROM users WHERE EMAIL = '{mail}'")
        return ibm_db.fetch_row(stmt)
    
    def new_agent(self, name: str, mail: str, password: str, role: str) -> bool:
        try:
            ibm_db.exec_immediate(self.conn, 
                                "INSERT INTO agents (name, email, password, role) VALUES ('{}', '{}', '{}', '{}')".format(name, mail, password, role))
        except Exception as e:
            print(e)
            return False
        return True
    
    def check_agent_exists(self, mail: str) -> bool:
        stmt = ibm_db.exec_immediate(self.conn, "SELECT * FROM agents WHERE EMAIL = '{}'".format(mail))
        return ibm_db.fetch_row(stmt)
    
    def check_agent(self, mail: str, password: str) -> bool:
        stmt = ibm_db.exec_immediate(self.conn, "SELECT * FROM agents WHERE EMAIL = '{}' AND PASSWORD = '{}'".format(mail, password))
        return ibm_db.fetch_row(stmt)
    
    def new_admin(self, name: str, mail: str, password: str) -> bool:
        try:
            ibm_db.exec_immediate(self.conn, "INSERT INTO admins (name, email, password) VALUES ('{}', '{}', '{}')".format(name, mail, password))
        except Exception as e:
            print(e)
            return False
        return True
    
    def check_admin(self, mail: str, password: str) -> bool:
        stmt = ibm_db.exec_immediate(self.conn, "SELECT * FROM admins WHERE EMAIL = '{}' AND PASSWORD = '{}'".format(mail, password))
        return ibm_db.fetch_row(stmt)
    
    def check_admin_exists(self, mail: str) -> bool:
        stmt = ibm_db.exec_immediate(self.conn, "SELECT * FROM admins WHERE EMAIL = '{}'".format(mail))
        return ibm_db.fetch_row(stmt)
    
    def new_complaint(self, title: str, description: str, mail: str, image_url: str, latitute: str, longitute: str, location_details: str, ticketid: str) -> bool:
        
        try:
            query = "INSERT INTO complaints (email, image_url, title, description, location_details, latitute, longitute, ticket_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
            query = query.format(
                mail, image_url, title, description, location_details, latitute, longitute, ticketid)

            ibm_db.exec_immediate(self.conn, query)
            return True
        except Exception as e:
            print(e)
            return False

    def get_tasks(self, agentid: str):
        try:
            query = "SELECT * FROM complaints WHERE ASSIGNEE = '{}'".format(agentid)
            stmt = ibm_db.exec_immediate(self.conn, query)
            result = ibm_db.fetch_assoc(stmt)
            complaints = []
            while result:
                complaints.append(result)
                result = ibm_db.fetch_assoc(stmt)
            return complaints
        except Exception as e:
            print(e, "is the error")
            return []

    def get_all_complaints(self) -> list:
        stmt = ibm_db.exec_immediate(self.conn, "SELECT * FROM complaints")
        result = ibm_db.fetch_assoc(stmt)
        complaints = []
        while result:
                complaints.append(result)
                result = ibm_db.fetch_assoc(stmt)
        return complaints
    
    def get_user_complaints(self, mail: str) -> list:
        stmt = ibm_db.exec_immediate(self.conn, "SELECT * FROM complaints WHERE EMAIL = '{}'".format(mail))
        result = ibm_db.fetch_assoc(stmt)
        complaints = []
        while result:
                complaints.append(result)
                result = ibm_db.fetch_assoc(stmt)
        return complaints
    
    def fetch_agents(self) -> list:
        stmt = ibm_db.exec_immediate(self.conn, "SELECT * FROM agents")
        result = ibm_db.fetch_assoc(stmt)
        agents = []
        while result:
                agents.append(result)
                result = ibm_db.fetch_assoc(stmt)
        return agents
    
    def assigntask(self, ticketid: str, agentid: str):
        try:
            query = "UPDATE complaints SET ASSIGNEE = '{}' WHERE TICKET_ID = '{}'".format(agentid, ticketid)
            ibm_db.exec_immediate(self.conn, query)
            return True
        except Exception as e:
            print(e)
            return False
    
    def deletecomplaint(self, ticketid: str):
        try:
            query = "DELETE FROM complaints WHERE TICKET_ID = '{}'".format(ticketid)
            ibm_db.exec_immediate(self.conn, query)
            return True
        except Exception as e:
            print(e)
            return False
    
    def update_status(self, ticketid: str, progress: str, imgafter: str) -> bool:
        try:
            query = "UPDATE complaints SET PROGRESS = '{}', IMAGE_AFTER = '{}', STATUS = '{}' WHERE TICKET_ID = '{}'".format(progress, imgafter, "done", ticketid)
            ibm_db.exec_immediate(self.conn, query)
            return True
        except Exception as e:
            print(e)
            return False

    def setup_s3(self):
        try:
            cos = ibm_boto3.client(service_name='s3',
                                   ibm_api_key_id=COS_API_KEY_ID,
                                   ibm_service_instance_id=COS_RESOURCE_CRN,
                                   config=Config(signature_version='oauth'),
                                   endpoint_url=COS_ENDPOINT)
            return cos
        except Exception as e:
            print(e)
            return None

    def upload_file(self, path: str) -> str:
        try:
            self.cos.upload_file(
                Filename=path, Bucket=COS_BUCKET_NAME, Key=path)
            return f"{COS_ENDPOINT}/{COS_BUCKET_NAME}/{path}"
        except Exception as e:
            print(e)
            return None

    def generate_random_string(self, length: int):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    


func = Functions()
