import { useQuery } from "@tanstack/react-query";
import { getCommentsofTodo } from "../services/posts";
import { useState } from "react";

function PostComments() {
    const [id, setId] = useState(1);

    const handleNextPost = () => {
        setId((prev) => prev + 1);
    };

    const resetCount = () => {
        setId(1)
    }

    const { data, isLoading, isError, error, isFetching, refetch } = useQuery({
        queryKey: ["getComments", id],  // Tanstack wouldnt know which cache for which query if we dont pass the id
        queryFn: () => getCommentsofTodo(id),
        keepPreviousData: true,
    });

    return (
        <div>
            <h2>Comments for Post {id}</h2>

            {isFetching && <p>Fetching new comments...</p>}
            {isLoading && <p>Loading...</p>}
            {isError && <p>Error: {error.message}</p>}

            <ul>
                {data?.map((comment) => (
                    <li key={comment.id}>{comment.body}</li>
                ))}
            </ul>

            <button onClick={resetCount}> Reset </button>
            <button onClick={handleNextPost}>Next Post</button>
            <button onClick={() => refetch()}>Refetch</button>
        </div>
    );
}

export default PostComments;
