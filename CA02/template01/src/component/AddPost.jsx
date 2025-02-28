import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { addPost, postsQueryOptions } from "../services/posts"
import { samplePost } from "../data/posts";
import { useState } from "react";

export function AddPost() {

    const queryClient = useQueryClient();

    const { data, isLoading: isQueryLoading } = useQuery(postsQueryOptions)
  
    const [formData, setFormData] = useState({
        title: "",
        body: "",
        userId: samplePost.userId
    });

    function resetForm() {
        setFormData({
            title: "",
            body: "",
            userId: samplePost.userId
        })
    }
    
    const { mutate, isLoading: isMutationLoading, isError, error } = useMutation({
        mutationFn: () => addPost(formData),
        onSuccess: (data) => {
            console.log("Post added successfully:", data);
            resetForm();
            queryClient.setQueriesData(['getAllPosts'], (oldPosts) => [...oldPosts, samplePost])
            // queryClient.invalidateQueries(['getAllPosts']);  // This is like a later trigger to get newe data frm api, cache is marked invalid, upon next request new data will be refetched
        },
        onError: (error) => {
            console.error("Error adding post:", error);
        }
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        mutate();
    };

    return (
        <div>
            <h2>Add New Post</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="title">Title:</label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        disabled={isMutationLoading}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="body">Body:</label>
                    <textarea
                        id="body"
                        name="body"
                        value={formData.body}
                        onChange={handleChange}
                        disabled={isMutationLoading}
                        required
                    />
                </div>
                <button type="submit" disabled={isMutationLoading}>
                    {isMutationLoading ? "Adding..." : "Add Post"}
                </button>
                {isError && (
                    <p style={{ color: "red" }}>
                        Error: {error.message || "Failed to add post"}
                    </p>
                )}
            </form>

            <div>
                <h3>All Posts</h3>
                {isQueryLoading ? (
                    <p>Loading posts...</p>
                ) : (
                    <table style={{ width: "100%", borderCollapse: "collapse" }}>
                        <thead>
                            <tr>
                                <th style={{ border: "1px solid black", padding: "8px" }}>ID</th>
                                <th style={{ border: "1px solid black", padding: "8px" }}>Title</th>
                                <th style={{ border: "1px solid black", padding: "8px" }}>Body</th>
                                <th style={{ border: "1px solid black", padding: "8px" }}>User ID</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data?.map((post) => (
                                <tr key={post.id}>
                                    <td style={{ border: "1px solid black", padding: "8px" }}>{post.id}</td>
                                    <td style={{ border: "1px solid black", padding: "8px" }}>{post.title}</td>
                                    <td style={{ border: "1px solid black", padding: "8px" }}>{post.body}</td>
                                    <td style={{ border: "1px solid black", padding: "8px" }}>{post.userId}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}
