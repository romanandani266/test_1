import React, { useEffect, useState } from "react";
import { getBlogs } from "../api";
import { Link } from "react-router-dom";
import { Container, Typography, Card, CardContent, Button } from "@mui/material";

const BlogList = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const data = await getBlogs();
        setBlogs(data);
      } catch (error) {
        console.error("Error fetching blogs:", error);
      }
    };
    fetchBlogs();
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Blog List
      </Typography>
      {blogs.map((blog) => (
        <Card key={blog.id} sx={{ marginBottom: 2 }}>
          <CardContent>
            <Typography variant="h5">{blog.title}</Typography>
            <Typography variant="body2">{blog.content.substring(0, 100)}...</Typography>
            <Button component={Link} to={`/blogs/${blog.id}`}>
              Read More
            </Button>
          </CardContent>
        </Card>
      ))}
    </Container>
  );
};

export default BlogList;
