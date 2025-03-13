import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Typography, Box } from "@mui/material";
import { getBlogById } from "../api";

const BlogDetailPage = () => {
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
    <Box padding={2}>
      <Typography variant="h3" gutterBottom>
        {blog.title}
      </Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: "100%", maxHeight: "400px" }} />
      <Typography variant="body1" paragraph>
        {blog.content}
      </Typography>
      <Typography variant="caption">Created at: {new Date(blog.created_at).toLocaleString()}</Typography>
    </Box>
  );
};

export default BlogDetailPage;
