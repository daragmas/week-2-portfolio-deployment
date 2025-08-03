#tests/test_app.py

import unittest
import os
import re
from pprint import pprint

os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellows</title>" in html
        assert "Nathaniel Wolf" in html
    #    assert "Anitha Amarnath" in html
        
    def test_timeline_get(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
    
    def test_timeline_post_and_get(self):
        post_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'content': 'This is a test post'
        }
        
        # assert body fields of post response, this is part of the test
        response = self.client.post("/api/timeline_post", data=post_data)
        assert response.status_code == 200
        assert response.is_json
        response_data = response.get_json()
        assert response_data['name'] == 'Test User'
        assert response_data['email'] == 'test@example.com'
        assert response_data['content'] == 'This is a test post'
        
        # fetch all timeline posts, look at topmost
        # since in testing environment, guaranteed top most is previously created post
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        response_json = response.get_json()
        assert len(response_json["timeline_posts"]) == 1
        test_post = response_json["timeline_posts"][0]
        assert test_post['name'] == 'Test User'
        assert test_post['email'] == 'test@example.com'
        assert test_post['content'] == 'This is a test post'

        response = self.client.get("/timeline")
        expected = f"""<div class="row mb-3 p-3 border rounded shadow-sm bg-light">
    <!-- Left Column: Gravatar + Name/Email -->
    <div class="col-md-3 d-flex align-items-start">
        <img src="https://secure.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0?s=60&amp;d=identicon&amp;r=g" class="rounded-circle me-3" width="60" height="60" alt="Avatar">
        <div>
            <strong>Test User</strong><br>
            <small class="text-muted">test@example.com</small>
        </div>
    </div>

    <!-- Right Column: Post Content -->
    <div class="col-md-9">
        <p class="mb-2">This is a test post</p>
        <small class="text-muted">{test_post['created_at']}</small>
    </div>
</div>"""       # really odd solution for comparison actually guarantees all of this data was in one entry

        expected_arr = expected.split("\n")
        html_arr = response.get_data(as_text=True).split("\n")
        # print("Expected Array:")
        # pprint(expected_arr[0])
        # print("HTML Array:")
        # pprint(html_arr)
        # print("HTML_arr: ", len(html_arr), " Expected Arr: ", len(expected_arr))
        
        # go until we're at the right block, top post would be the test post above
        # i = 0
        # while html_arr[i].strip() != expected_arr[0].strip():
        #     # print(i)  
        #     i += 1
        
        # # iterate through and assert all html lines match
        # for j in range(len(expected_arr)):
        #     # switch datetime format of relevant line to compare correctly
        #     timestamp_match = re.search(r'<small class="text-muted">2025(.*?)</small>', html_arr[j+i].strip())
        #     if timestamp_match:
        #         original_timestamp = "2025" + timestamp_match.group(1)
        #         from datetime import datetime
        #         dt = datetime.strptime(original_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        #         formatted_timestamp = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
        #         html_arr[j+i] = f'<small class="text-muted">{formatted_timestamp}</small>'
            
        #     assert expected_arr[j].strip()==html_arr[j+i].strip()
            

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data= {"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True) 
        assert "Invalid Name" in html
        
        # POST request with empty content
        response = self.client.post("/api/timeline_post", data= {"name": "John Doe", "email": "john@example.com", "content":""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html
        
        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data= {"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html