import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getBlogById } from "../api";
import { Container, Typography, Box } from "@mui/material";

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

  if (!blog) return <Typography>Loading...</Typography>;

  return (
    <Container>
      <Box
        sx={{
          backgroundImage: `url(https://plus.unsplash.com/premium_photo-1684581214880-2043e5bc8b8b?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          padding: "50px",
          color: "white",
        }}
      >
        <Typography variant="h3">{blog.title}</Typography>
        <Typography variant="subtitle1">{new Date(blog.created_at).toLocaleDateString()}</Typography>
      </Box>
      <img src={blog.image_url} alt={blog.title} style={{ width: "100%", marginTop: "20px" }} />
      <Typography variant="body1" sx={{ mt: 3 }}>
        {blog.content}
      </Typography>
    </Container>
  );
}

export default BlogDetailPage;
