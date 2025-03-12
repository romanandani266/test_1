import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { createBlog, updateBlog, getBlogById } from "../api";
import BlogForm from "../components/BlogForm";

function CreateEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [blog, setBlog] = useState({ title: "", content: "", image_url: "" });

  useEffect(() => {
    if (id) {
      const fetchBlog = async () => {
        try {
          const data = await getBlogById(id);
          setBlog(data);
        } catch (error) {
          console.error("Error fetching blog:", error);
        }
      };
      fetchBlog();
    }
  }, [id]);

  const handleSubmit = async (formData) => {
    try {
      if (id) {
        await updateBlog(id, formData);
      } else {
        await createBlog(formData);
      }
      navigate("/");
    } catch (error) {
      console.error("Error saving blog:", error);
    }
  };

  return <BlogForm blog={blog} onSubmit={handleSubmit} />;
}

export default CreateEditPage;
