import { useQuery } from "@tanstack/react-query";
import { getTodos } from "../services/todos"

function TodoList() {
    
    const { data, isLoading, isError, error, isFetching, refetch } = useQuery({
        queryKey: ["getTodos"],
        queryFn: getTodos,
    });

    if (isFetching) return <p> Fetching...</p>
    if (isLoading) return <p>Loading...</p>;
    if (isError) return <p>Error: {(error).message}</p>;

    return (
        <div>
            <ul>
                {data.map((todo) => (
                    <li key={todo.id}>{todo.title}</li>
                ))}
            </ul>

            <button onClick={refetch}> Refetch </button>
        </div>
    );
}

export default TodoList;
