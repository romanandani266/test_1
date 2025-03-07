import React from "react";
import { Card, CardMedia, CardContent, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";

const BlogCard = ({ blog }) => {
  return (
    <Card>
      <CardMedia component="img" height="140" image={blog.image_url} alt={blog.title} />
      <CardContent>
        <Typography variant="h6">{blog.title}</Typography>
        <Typography variant="body2" color="text.secondary">
          {blog.content.substring(0, 100)}...
        </Typography>
        <Button component={Link} to={`/blogs/${blog.id}`} size="small">
          Read More
        </Button>
      </CardContent>
    </Card>
  );
};

export default BlogCard;