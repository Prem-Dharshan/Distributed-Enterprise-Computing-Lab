import { useState, ChangeEvent, FormEvent } from "react";
import { FaSearch } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { Input } from "./ui/input";

const Search: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState<string>("");
  const navigate = useNavigate();

  const submitHandler = (e: FormEvent) => {
    e.preventDefault();
    if (searchTerm) {
      navigate(`/searched/${searchTerm}`);
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <form
      onSubmit={submitHandler}
      className="mx-8 my-4 max-w-lg w-full relative"
    >
      <div className="relative w-full">
        <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white" />
        <Input
          type="text"
          value={searchTerm}
          onChange={handleChange}
          className="bg-gradient-to-r from-gray-700 to-gray-800 text-white text-lg py-3 pl-12 pr-4 rounded-lg w-full"
          placeholder="Search for recipes..."
        />
      </div>
    </form>
  );
};

export default Search;
