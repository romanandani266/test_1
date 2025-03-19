import React, { useEffect, useState } from "react";
import { fetchBlogs } from "../services/api";
import { Link } from "react-router-dom";
import { Card, CardContent, Typography, Button } from "@mui/material";

const BlogList = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const loadBlogs = async () => {
      try {
        const data = await fetchBlogs();
        setBlogs(data);
      } catch (error) {
        console.error("Error loading blogs:", error);
      }
    };
    loadBlogs();
  }, []);

  return (
    <div>
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
    </div>
  );
};

export default BlogList;
