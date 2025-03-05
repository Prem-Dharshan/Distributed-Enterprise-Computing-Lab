import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

interface Recipe {
  id: number;
  title: string;
  image: string;
}

const Searched = () => {
    const apiKey = import.meta.env.VITE_SPOONACULAR_API_KEY;
  const { search } = useParams(); // Corrected the typo from `parmas` to `search`

  // Fetch searched recipes with TanStack Query and Axios
  const {
    data: searchedRecipes,
    isLoading,
    error,
  } = useQuery<Recipe[]>({
    queryKey: ["searchedRecipes", search],
    queryFn: async () => {
      const resp = await axios.get(
        `https://api.spoonacular.com/recipes/complexSearch?apiKey=${apiKey}&query=${search}`
      );
      return resp.data.results;
    },

    enabled: !!search, // Only run the query if search term exists
  });

  // Handle loading and error states
  if (isLoading) return <p className="text-center">Loading...</p>;
  if (error)
    return <p className="text-center text-red-500">Failed to load recipes.</p>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
      {searchedRecipes?.map(({ title, id, image }) => (
        <div key={id} className="max-w-sm rounded-lg shadow-md overflow-hidden">
          <Link to={`/recipe/${id}`}>
            <img
              src={image}
              alt={title}
              className="w-full h-48 object-cover rounded-t-lg"
            />
            <div className="p-4">
              <h4 className="text-lg font-bold">{title}</h4>
            </div>
          </Link>
        </div>
      ))}
    </div>
  );
};

export default Searched;
