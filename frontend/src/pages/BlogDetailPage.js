import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getBlogById } from "../api";
import { Typography, Container } from "@mui/material";

function BlogDetailPage() {
  const { id } = useParams();
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

  if (!blog) return <div>Loading...</div>;

  return (
    <Container style={{ padding: "20px", backgroundImage: `url(https://plus.unsplash.com/premium_photo-1684581214880-2043e5bc8b8b?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)` }}>
      <Typography variant="h3" style={{ marginBottom: "20px" }}>
        {blog.title}
      </Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: "100%", marginBottom: "20px" }} />
      <Typography variant="body1">{blog.content}</Typography>
      <Typography variant="caption" display="block" style={{ marginTop: "20px" }}>
        Created At: {new Date(blog.created_at).toLocaleString()}
      </Typography>
    </Container>
  );
}

export default BlogDetailPage;
