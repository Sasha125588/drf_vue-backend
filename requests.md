# API Testing Guide for Postman

## Environment Setup

Create these environment variables in Postman:

- `base_url`: `http://127.0.0.1:8000`
- `access_token`: (leave empty)
- `refresh_token`: (leave empty)

## User Authentication Endpoints

### 1. Register User

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/register/`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "username": "testuser123",
  "email": "test@example.com",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "first_name": "Test",
  "last_name": "User"
}
```

### 2. Login

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/login/`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "email": "test@example.com",
  "password": "SecurePassword123!"
}
```

### 3. Get Profile

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`

### 4. Update Profile

- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "first_name": "Updated Test",
  "last_name": "Updated User",
  "bio": "This is my updated bio"
}
```

### 5. Update Avatar

- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Body:** (form-data)
  - `avatar`: [select image file]
  - `bio`: "Updated bio with avatar"

### 6. Change Password

- **Method:** PUT
- **URL:** `{{base_url}}/api/v1/auth/change-password/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "old_password": "SecurePassword123!",
  "new_password": "NewSecurePassword456!",
  "new_password_confirm": "NewSecurePassword456!"
}
```

### 7. Refresh Token

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/token/refresh/`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "refresh": "{{refresh_token}}"
}
```

### 8. Logout

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/logout/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "refresh_token": "{{refresh_token}}"
}
```

## Category Endpoints

### 9. Get All Categories

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/posts/categories/`
- **Headers:** None required
- **Query Parameters (optional):**
  - `search`: search in name and description
  - `ordering`: `name`, `created_at`, `-name`, `-created_at`

### 10. Create Category

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/posts/categories/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "name": "Technology",
  "description": "Articles about technology and programming"
}
```

### 11. Get Category Details

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/posts/categories/technology/`
- **Headers:** None required

### 12. Update Category

- **Method:** PUT
- **URL:** `{{base_url}}/api/v1/posts/categories/technology/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "name": "Advanced Technology",
  "description": "Advanced articles about technology and programming"
}
```

### 13. Delete Category

- **Method:** DELETE
- **URL:** `{{base_url}}/api/v1/posts/categories/technology/`
- **Headers:** `Authorization: Bearer {{access_token}}`

### 14. Get Posts by Category

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/posts/categories/technology/posts/`
- **Headers:** None required

## Post Endpoints

### 15. Get All Posts

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/posts/`
- **Headers:** None required
- **Query Parameters (optional):**
  - `category`: filter by category ID
  - `author`: filter by author ID
  - `status`: filter by status (`draft` or `published`)
  - `search`: search in title and content
  - `ordering`: `title`, `created_at`, `updated_at`, `views_count`, `-title`, `-created_at`, `-updated_at`, `-views_count`
  - `page`: page number for pagination

### 16. Create Post

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/posts/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "title": "My First Post",
  "content": "This is the content of my first post. It contains detailed information about the topic.",
  "category": 1,
  "status": "published"
}
```

### 17. Create Post with Image

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/posts/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Body:** (form-data)
  - `title`: "Post with Image"
  - `content`: "This post has an image attached"
  - `category`: 1
  - `status`: "published"
  - `image`: [select image file]

### 18. Get Post Details

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/posts/my-first-post/`
- **Headers:** None required
- **Note:** This will increment the view count

### 19. Update Post

- **Method:** PUT
- **URL:** `{{base_url}}/api/v1/posts/my-first-post/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "title": "My Updated First Post",
  "content": "This is the updated content of my first post.",
  "category": 1,
  "status": "published"
}
```

### 20. Partial Update Post

- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/posts/my-first-post/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "content": "Just updating the content"
}
```

### 21. Delete Post

- **Method:** DELETE
- **URL:** `{{base_url}}/api/v1/posts/my-first-post/`
- **Headers:** `Authorization: Bearer {{access_token}}`

### 22. Get My Posts

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/posts/my-posts/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Query Parameters (optional):**
  - `category`: filter by category ID
  - `status`: filter by status (`draft` or `published`)
  - `search`: search in title and content
  - `ordering`: `title`, `created_at`, `updated_at`, `views_count`

### 23. Get Popular Posts

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/posts/popular/`
- **Headers:** None required

### 24. Get Recent Posts

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/posts/recent/`
- **Headers:** None required

## Sample Post Data for Testing

### Creating Multiple Categories

```json
[
  {
    "name": "Technology",
    "description": "Tech news and tutorials"
  },
  {
    "name": "Science",
    "description": "Scientific discoveries and research"
  },
  {
    "name": "Programming",
    "description": "Programming tutorials and tips"
  }
]
```

### Creating Multiple Posts

```json
[
  {
    "title": "Introduction to Django REST Framework",
    "content": "Django REST Framework is a powerful toolkit for building Web APIs in Django...",
    "category": 1,
    "status": "published"
  },
  {
    "title": "Python Best Practices",
    "content": "Here are some best practices when writing Python code...",
    "category": 3,
    "status": "published"
  },
  {
    "title": "Draft Article",
    "content": "This is a draft article that is not yet published...",
    "category": 2,
    "status": "draft"
  }
]
```

## Common Error Responses

### Invalid Credentials (401)

```json
{
  "non_field_errors": ["Invalid credentials"]
}
```

### Missing Token (401)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Expired Token (401)

```json
{
  "detail": "Given token not valid for any token type"
}
```

### Permission Denied (403)

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Not Found (404)

```json
{
  "detail": "Not found."
}
```

### Validation Errors (400)

```json
{
  "title": ["post with this title already exists."],
  "category": ["This field is required."]
}
```

### Unique Constraint Error (400)

```json
{
  "name": ["category with this name already exists."]
}
```

## Testing Flow

### Complete Testing Sequence

1. **Setup:**

   - Register a new user
   - Login to get tokens

2. **Categories:**

   - Create several categories
   - List all categories
   - Get category details
   - Update a category
   - Get posts by category

3. **Posts:**

   - Create posts in different categories
   - List all posts (test filtering and searching)
   - Get post details (check view count increment)
   - Update your own posts
   - Try to update someone else's post (should fail)
   - Get your own posts
   - Get popular posts
   - Get recent posts

4. **Cleanup:**
   - Delete test posts
   - Delete test categories
   - Logout

### Testing Permissions

1. **Anonymous User:**

   - Can view published posts and categories
   - Cannot create, update, or delete anything

2. **Authenticated User:**

   - Can create posts and categories
   - Can only update/delete their own posts
   - Can update/delete any category (you might want to restrict this)

3. **Author Permissions:**
   - Can see their own draft posts in listings
   - Can update their published and draft posts
   - Cannot update other users' posts

## Comment Endpoints

### 25. Get All Comments

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/comments/`
- **Headers:** None required
- **Query Parameters (optional):**
  - `post`: filter by post ID
  - `author`: filter by author ID
  - `parent`: filter by parent comment ID (null for main comments)
  - `search`: search in comment content
  - `ordering`: `created_at`, `updated_at`, `-created_at`, `-updated_at`
  - `page`: page number for pagination

### 26. Create Comment

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/comments/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "content": "This is a great article! Thanks for sharing.",
  "post": 1,
  "parent": null
}
```

### 27. Create Reply to Comment

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/comments/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "content": "I totally agree with your comment!",
  "post": 1,
  "parent": 5
}
```

### 28. Get Comment Details

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/comments/1/`
- **Headers:** None required
- **Note:** This will show the comment with all its replies

### 29. Update Comment

- **Method:** PUT
- **URL:** `{{base_url}}/api/v1/comments/1/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "content": "This is my updated comment content."
}
```

### 30. Partial Update Comment

- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/comments/1/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "content": "Just updating the comment text"
}
```

### 31. Delete Comment (Soft Delete)

- **Method:** DELETE
- **URL:** `{{base_url}}/api/v1/comments/1/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Note:** This performs a soft delete (sets is_active=False)

### 32. Get My Comments

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/comments/my-comments/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Query Parameters (optional):**
  - `post`: filter by post ID
  - `parent`: filter by parent comment ID
  - `is_active`: filter by active status (true/false)
  - `search`: search in comment content
  - `ordering`: `created_at`, `updated_at`, `-created_at`, `-updated_at`

### 33. Get Comments for Specific Post

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/comments/post/1/`
- **Headers:** None required
- **Note:** Returns only main comments (not replies) for the post

### 34. Get Replies for Specific Comment

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/comments/comment/5/replies/`
- **Headers:** None required
- **Note:** Returns all replies to a specific comment

## Sample Comment Data for Testing

### Creating Main Comments

```json
[
  {
    "content": "Excellent article! Very informative and well-written.",
    "post": 1,
    "parent": null
  },
  {
    "content": "I have a question about the implementation details...",
    "post": 1,
    "parent": null
  },
  {
    "content": "This helped me solve a problem I was having. Thank you!",
    "post": 2,
    "parent": null
  }
]
```

### Creating Replies

```json
[
  {
    "content": "I'm glad you found it helpful!",
    "post": 1,
    "parent": 1
  },
  {
    "content": "Feel free to ask any specific questions.",
    "post": 1,
    "parent": 2
  },
  {
    "content": "What specific part are you referring to?",
    "post": 1,
    "parent": 2
  }
]
```

## Extended Error Responses for Comments

### Invalid Post Reference (400)

```json
{
  "non_field_errors": ["Post is not published"]
}
```

### Invalid Parent Comment (400)

```json
{
  "parent": ["Parent does not match"]
}
```

### Comment Not Found (404)

```json
{
  "detail": "Not found."
}
```

### Cannot Modify Other User's Comment (403)

```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Extended Testing Flow

### Complete Testing Sequence with Comments

1. **Setup:**

   - Register a new user
   - Login to get tokens
   - Create categories and posts

2. **Categories & Posts:**

   - Create several categories
   - Create posts in different categories
   - List all posts

3. **Comments:**

   - Create main comments on different posts
   - Create replies to existing comments
   - List all comments (test filtering)
   - Get comments for specific post
   - Get replies for specific comment
   - Update your own comments
   - Try to update someone else's comment (should fail)
   - Get your own comments
   - Test nested comment structure

4. **Advanced Comment Testing:**

   - Create comment chains (reply to replies)
   - Test comment permissions
   - Test soft delete functionality
   - Test comment counting on posts

5. **Cleanup:**
   - Delete test comments
   - Delete test posts
   - Delete test categories
   - Logout

### Testing Comment Permissions

1. **Anonymous User:**

   - Can view active comments on published posts
   - Cannot create, update, or delete comments
   - Cannot view inactive comments

2. **Authenticated User:**

   - Can create comments on published posts
   - Can only update/delete their own comments
   - Can reply to any active comment
   - Can view all their own comments (including inactive)

3. **Comment Author:**
   - Can edit their own comments
   - Can soft-delete their own comments
   - Cannot modify other users' comments

### Comment-Specific Testing Scenarios

1. **Nested Comments:**

   - Create a main comment
   - Reply to that comment
   - Reply to the reply (3 levels deep)
   - Verify proper parent-child relationships

2. **Comment Validation:**

   - Try to comment on a draft post (should fail)
   - Try to reply with wrong post ID (should fail)
   - Try to create empty comment (should fail)

3. **Comment Counting:**

   - Create several comments on a post
   - Verify the comment count is correct
   - Soft-delete a comment
   - Verify the count decreases

4. **Search and Filtering:**
   - Search comments by content
   - Filter comments by post
   - Filter comments by author
   - Filter main comments vs replies

## Notes

- All timestamps are in UTC
- Post slugs are automatically generated from titles
- Category slugs are automatically generated from names
- View counts are incremented on each GET request to post detail
- Only published posts are shown to anonymous users
- Only active comments are shown to anonymous users
- Comment deletion is soft delete (sets is_active=False)
- Comments can be nested (replies to replies)
- Search functionality works across title and content fields for posts and comments
- Pagination is set to 20 items per page by default
- Comment replies are loaded when getting comment details
- Comments are ordered by creation date (newest first) by default
