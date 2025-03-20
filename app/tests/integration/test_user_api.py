import json
from app.models.user import User

async def test_user_registration_mutation(client):
    # First ensure the test user doesn't exist
    query = """
    mutation {
        user_registration(
            user: {
                email: "newtest1@example.com",
                password: "password123",
                first_name: "Test",
                last_name: "User"
            }
        ) {
            message
            user {
                email
                first_name
            }
        }
    }
    """
    
    response = client.post(
        "/graphql",
        json={"query": query}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    assert data["data"]["user_registration"]["message"] == "User registered successfully"
    assert data["data"]["user_registration"]["user"]["email"] == "newtest1@example.com"

def test_user_login_mutation(client):
    query = """
    mutation {
        user_login(
            user: {
                email: "newtest1@example.com",
                password: "password123"
            }
        ) {
            access_token
            refresh_token
            token_type
            user {
                email
                first_name
                last_name
            }
        }
    }
    """
    
    response = client.post(
        "/graphql",
        json={"query": query}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    assert data["data"]["user_login"]["token_type"] == "Bearer"
    assert data["data"]["user_login"]["user"]["email"] == "newtest1@example.com"

# def test_users_query(client, test_user):
#     # First, login to get the token
#     login_query = """
#     mutation {
#         user_login(
#             user: {
#                 email: "test@example.com",
#                 password: "password123"
#             }
#         ) {
#             accessToken
#         }
#     }
#     """
    
#     login_response = client.post(
#         "/graphql",
#         json={"query": login_query}
#     )
    
#     token = login_response.json()["data"]["user_login"]["accessToken"]
    
#     # Now query the users endpoint
#     query = """
#     query {
#         users(page: 1, perPage: 10) {
#             items {
#                 email
#                 firstName
#                 lastName
#             }
#             pageInfo {
#                 totalItems
#                 currentPage
#                 perPage
#             }
#         }
#     }
#     """
    
#     response = client.post(
#         "/graphql",
#         json={"query": query},
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert "errors" not in data
#     assert len(data["data"]["users"]["items"]) > 0
#     assert data["data"]["users"]["pageInfo"]["currentPage"] == 1 