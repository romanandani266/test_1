import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getBlog } from "../api";
import { Container, Typography } from "@mui/material";

const BlogDetail = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const fetchBlog = async () => {
      try {
        const data = await getBlog(id);
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
      <Typography variant="h4">{blog.title}</Typography>
      <Typography variant="body1">{blog.content}</Typography>
    </Container>
  );
};

export default BlogDetail;
