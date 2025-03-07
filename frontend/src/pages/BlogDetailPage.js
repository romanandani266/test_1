import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Typography, Button, Box } from "@mui/material";
import { getBlogById, deleteBlog } from "../api";

const BlogDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const fetchBlog = async () => {
      try {
        const data = await getBlogById(id);
        setBlog(data);
      } catch (error) {
        console.error("Error fetching blog:", error);
      }
    };
    fetchBlog();
  }, [id]);

  const handleDelete = async () => {
    try {
      await deleteBlog(id);
      navigate("/");
    } catch (error) {
      console.error("Error deleting blog:", error);
    }
  };

  if (!blog) return <Typography>Loading...</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        {blog.title}
      </Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: "100%", marginBottom: "16px" }} />
      <Typography variant="body1" gutterBottom>
        {blog.content}
      </Typography>
      <Typography variant="caption" display="block" gutterBottom>
        Created At: {new Date(blog.created_at).toLocaleString()}
      </Typography>
      <Button variant="contained" color="secondary" onClick={handleDelete}>
        Delete Blog
      </Button>
    </Box>
  );
};

export default BlogDetailPage;
