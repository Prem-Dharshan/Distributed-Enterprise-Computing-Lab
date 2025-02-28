import axios from "axios";

export const getCommentsofTodo = async (id) => {
    try {
        const response = await axios.get(`https://jsonplaceholder.typicode.com/comments?postId=${id}`);
        return response.data;
    } catch (error) {
        throw new Error("Failed to fetch comments.");
    }
};


export const addPost = async (newPost) => {
    const response = await axios.post("https://jsonplaceholder.typicode.com/posts", newPost);
    return response.data;
}


export const getAllPosts = async () => {
    const response = await axios.get("https://jsonplaceholder.typicode.com/posts");
    return response.data;
}


export const postsQueryOptions = {
    queryKey: ['getAllPosts'],
    queryFn: getAllPosts,
    staleTime: 5 * 60 * 1000,
    cacheTime: 30 * 60 * 1000,
    retry: 2,
    refetchInterval: 1 * 60 * 1000,
    gcTime:  10 * 60 * 1000,
    enabled: true   // Use some state for conditonal rendering   
};
