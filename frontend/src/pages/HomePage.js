import React, { useEffect, useState } from "react";
import { Grid } from "@mui/material";
import BlogCard from "../components/BlogCard";
import { getAllBlogs } from "../api";
#comment

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
    <Grid container spacing={2} sx={{ padding: 2 }}>
      {blogs.map((blog) => (
        <Grid item xs={12} sm={6} md={4} key={blog.id}>
          <BlogCard blog={blog} />
        </Grid>
      ))}
    </Grid>
  );
};

export default HomePage;
