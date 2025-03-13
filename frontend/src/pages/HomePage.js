import React, { useEffect, useState } from "react";
import { Grid, Card, CardMedia, CardContent, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";
import { getAllBlogs } from "../api";

const HomePage = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const data = await getAllBlogs();
        setBlogs(data);
      } catch (error) {
        console.error("Error fetching blogs:", error);
      }
    };
    fetchBlogs();
  }, []);

  return (
    <Grid container spacing={2} padding={2}>
      {blogs.map((blog) => (
        <Grid item xs={12} sm={6} md={4} key={blog.id}>
          <Card>
            <CardMedia component="img" height="140" image={blog.image_url} alt={blog.title} />
            <CardContent>
              <Typography variant="h6">{blog.title}</Typography>
              <Typography variant="body2">{blog.content.substring(0, 100)}...</Typography>
              <Button component={Link} to={`/blogs/${blog.id}`} size="small">
                Read More
              </Button>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default HomePage;
