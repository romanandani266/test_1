import React from 'react';
import { Card, CardContent, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';

const BlogList = ({ blogs }) => {
  return (
    <div>
      {blogs.map((blog) => (
        <Card key={blog.id} sx={{ marginBottom: 2 }}>
          <CardContent>
            <Typography variant="h5">{blog.title}</Typography>
            <Typography variant="body2">{blog.content.substring(0, 100)}...</Typography>
            <Button component={Link} to={`/view/${blog.id}`} color="primary">
              View
            </Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default BlogList;
