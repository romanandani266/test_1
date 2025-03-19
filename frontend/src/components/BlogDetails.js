import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchBlogById } from "../api";
import { Typography } from "@mui/material";

const BlogDetails = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const loadBlog = async () => {
      try {
        const data = await fetchBlogById(id);
        setBlog(data);
      } catch (error) {
        console.error("Error loading blog:", error);
      }
    };
    loadBlog();
  }, [id]);

  if (!blog) return <Typography>Loading...</Typography>;

  return (
    <div>
      <Typography variant="h4">{blog.title}</Typography>
      <Typography variant="body1">{blog.content}</Typography>
    </div>
  );
};

export default BlogDetails;
