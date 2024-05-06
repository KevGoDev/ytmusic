import { useState } from 'react';
import { Container, Button, Box } from "@mui/material";
import IngredientsTable from './components/ingredient-list';
import AddIngredientsForm from './add-ingredient';

export type Ingredient = {
  name: string;
  category: string;
  image: string;
  quantity: string;
  quantity_unit: string;
  calories: string;
  protein: string;
}

const _MOCK_INGREDIENTS = [
  {
    name: "Egg(fried)",
    category: "protein",
    image: "https://ichef.bbci.co.uk/news/1024/cpsprodpb/7614/production/_105482203__105172250_gettyimages-857294664.jpg.webp",
    quantity: "1",
    quantity_unit: "unit",
    calories: "80",
    protein: "6",
  }
];

export default function IngredientsPage() {
  const [ingredients, setIngredients] = useState<Ingredient[]>(_MOCK_INGREDIENTS);
  const [isAddingNew, setIsAddingNew] = useState(true);
  
  const onAddNewIngredient = (newIngredient: Ingredient) => {
    setIngredients([...ingredients, newIngredient]);
    setIsAddingNew(false);
  }

  const toggleAddMode = () => {setIsAddingNew(prev => !prev)};

  // const handleAddIngredient = () => {
  //   if (!newIngredient) return;
  //   setIngredients([...ingredients, newIngredient]);
  //   setNewIngredient(null);
  //   handleClose();
  // };

  return (
    <Container>
      {/* Show table of ingredients */}
      {isAddingNew ? (
        <>
          <AddIngredientsForm createCallback={onAddNewIngredient}/>
        </>
      ) : (
        <>
          <IngredientsTable ingredients={ingredients}/>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Button variant="outlined" onClick={toggleAddMode}>Add Ingredient</Button>
          </Box>
        </>
      )}
    </Container>
  );
}