import { useState } from "react";
import { useParams } from "react-router-dom";
import { Button } from "@/components/ui/button"; // Assuming you have this component from ShadCN
import axios from "axios";
import { useQuery } from "@tanstack/react-query";

interface Ingredient {
  id: number;
  original: string;
}

interface RecipeDetails {
  title: string;
  image: string;
  summary: string;
  instructions: string;
  extendedIngredients: Ingredient[];
}

const Recipe = () => {
    const apiKey = import.meta.env.VITE_SPOONACULAR_API_KEY;
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState("instructions");

  // Fetch recipe details with Axios and TanStack
  const {
    data: details,
    isLoading,
    error,
  } = useQuery<RecipeDetails>({
    queryKey: ["recipeDetails", id],
    queryFn: async () => {
      const response = await axios.get(
        `https://api.spoonacular.com/recipes/${id}/information?apiKey=${apiKey}`
      );
      console.log(response)
      return response.data;
    },
    enabled: !!id, // Only run the query if id exists
  });

  // Handle loading and error states
  if (isLoading) return <p>Loading...</p>;
  if (error)
    return <p className="text-red-500">Failed to load recipe details.</p>;

  return (
    <div className="flex flex-col md:flex-row gap-10 mt-20">
      <div>
        <h2 className="text-3xl font-bold mb-4">{details?.title}</h2>
        <img
          src={details?.image}
          alt={details?.title}
          className="w-full rounded-xl"
        />
      </div>

      <div className="md:ml-10 flex-1">
        <div className="flex gap-4 mb-8">
          <Button
            variant={activeTab === "ingredients" ? "outline" : "default"} // Using available variants
            onClick={() => setActiveTab("ingredients")}
          >
            Ingredients
          </Button>
          <Button
            variant={activeTab === "instructions" ? "outline" : "default"} // Using available variants
            onClick={() => setActiveTab("instructions")}
          >
            Instructions
          </Button>
        </div>

        {activeTab === "ingredients" && (
          <ul className="space-y-2">
            {details?.extendedIngredients.map(({ id, original }) => (
              <li key={id} className="text-lg">
                {original}
              </li>
            ))}
          </ul>
        )}

        {activeTab === "instructions" && (
          <div>
            <p
              className="mt-4 text-lg"
              dangerouslySetInnerHTML={{ __html: details?.summary || "" }} // Added fallback value
            ></p>
            <p
              className="mt-4 text-lg"
              dangerouslySetInnerHTML={{ __html: details?.instructions || "" }} // Added fallback value
            ></p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recipe;
