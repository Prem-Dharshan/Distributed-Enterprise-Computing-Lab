import { FaPizzaSlice, FaHamburger } from "react-icons/fa";
import { GiNoodles, GiChopsticks } from "react-icons/gi";
import { NavLink } from "react-router-dom";
import { cn } from "@/lib/utils";

const categories = [
  { name: "Italian", icon: FaPizzaSlice, path: "/cuisines/Italian" },
  { name: "American", icon: FaHamburger, path: "/cuisines/American" },
  { name: "Thai", icon: GiNoodles, path: "/cuisines/Thai" },
  { name: "Japanese", icon: GiChopsticks, path: "/cuisines/Japanese" },
];

const Category: React.FC = () => {
  return (
    <div className="flex justify-center gap-6 py-4">
      {categories.map(({ name, icon: Icon, path }) => (
        <NavLink
          key={name}
          to={path}
          className={({ isActive }) =>
            cn(
              "flex flex-col items-center justify-center w-24 h-24 rounded-full transition-all",
              "bg-gradient-to-b from-gray-700 to-gray-900 hover:scale-105",
              isActive && "bg-gradient-to-r from-orange-500 to-pink-500"
            )
          }
        >
          <Icon className="text-white text-3xl" />
          <h4 className="text-white text-sm mt-2">{name}</h4>
        </NavLink>
      ))}
    </div>
  );
};

export default Category;