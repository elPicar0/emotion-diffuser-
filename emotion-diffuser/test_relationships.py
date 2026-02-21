
import http.client
import json

def test_relationship(relationship, text="I forgot your birthday, I am so sorry."):
    print(f"\n--- Testing Relationship: {relationship} ---")
    conn = http.client.HTTPConnection("127.0.0.1", 8000)
    payload = {
        "text": text,
        "relationship": relationship
    }
    headers = {'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/api/v1/apologize", json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read()
        if res.status == 200:
            res_data = json.loads(data.decode("utf-8"))
            print(f"Apology: {res_data['apology']}")
        else:
            print(f"Error: {res.status} - {data.decode('utf-8')}")
    except Exception as e:
        print(f"Request failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    relationships = ["parent", "friend", "professional"]
    for r in relationships:
        test_relationship(r)
