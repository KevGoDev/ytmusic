import { useState } from 'react';
import { Button, TextField, Box, Select, MenuItem, Stack, FormControl, InputLabel, styled, Paper } from "@mui/material";
import { Ingredient } from './ingredients';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';


const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

export default function AddIngredientsForm({ createCallback }: { createCallback: (newIngredient: Ingredient) => void }) {
  const [newIngredientName, setNewIngredientName] = useState<string>('');
  const [newIngredientCategory, setNewIngredientCategory] = useState<string>('');
  const [newIngredientImage, setNewIngredientImage] = useState<string>('');
  const [newIngredientQuantity, setNewIngredientQuantity] = useState<number>(0);
  const [newIngredientQuantityUnit, setNewIngredientQuantityUnit] = useState<string>('');
  const [newIngredientCalories, setNewIngredientCalories] = useState<number>(0);
  const [newIngredientProtein, setNewIngredientProtein] = useState<number>(0);

  const onAddNewIngredient = () => {
    
  }

  return (
    <Box
      component="form"
      noValidate
      autoComplete="off"
    >
      <Stack direction="column" spacing={2}>
        <Stack direction="row" spacing={2}>
          <TextField
            label="Name"
            placeholder='Egg(fried)'
            value={newIngredientName}
            onChange={(e) => setNewIngredientName(e.target.value)}
            sx={{flexGrow: 1, width: '50%'}}
          />
          <FormControl sx={{flexGrow: 1, width: '50%'}}>
            <InputLabel id="lbl-slt-cat">Category</InputLabel>
            <Select
              labelId="lbl-slt-cat"
              id="slt-cat"
              value={newIngredientCategory}
              label="Category"
              onChange={(e) => setNewIngredientCategory(e.target.value)}
            >
              <MenuItem value={10}>Protein</MenuItem>
              <MenuItem value={20}>Some nice dank food</MenuItem>
              <MenuItem value={30}>Thirty</MenuItem>
            </Select>
          </FormControl>
        </Stack>

        <Stack direction="row" spacing={2}>
          <TextField
            id="quantity"
            label="Quantity"
            type='number'
            value={newIngredientQuantity}
            onChange={(e) => setNewIngredientQuantity(e.target.value)}
            sx={{flexGrow: 1}}
          />
          <TextField
            id="quantity_unit"
            label="Unit"
            placeholder='mL, g, etc'
            value={newIngredientQuantityUnit}
            onChange={(e) => setNewIngredientQuantityUnit(e.target.value)}
            sx={{flexGrow: 1}}
          />
        </Stack>

        <Stack direction="row" spacing={2}>
          <TextField
            id="calories"
            label="Calories (kcal)"
            value={newIngredientCalories}
            onChange={(e) => setNewIngredientCalories(e.target.value)}
            sx={{flexGrow: 1}}
          />

          <TextField
            id="protein"
            label="Proteins (g)"
            value={newIngredientProtein}
            onChange={(e) => setNewIngredientProtein(e.target.value)}
            sx={{flexGrow: 1}}
          />
        </Stack>

        <Stack direction="column">
          <Paper variant="outlined">
            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
              <img 
                src="https://ichef.bbci.co.uk/news/1024/cpsprodpb/7614/production/_105482203__105172250_gettyimages-857294664.jpg.webp" 
                alt="Ingredient Image" 
                width={300} 
                height={200} 
                style={{ objectFit: 'cover' }} 
              />
            </Box>
          </Paper>          
          <Button
            component="label"
            variant="outlined"
            tabIndex={-1}
            startIcon={<CloudUploadIcon />}
          >
            Upload image
            <VisuallyHiddenInput type="file" />
          </Button>
        </Stack>

        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>          
          <Button variant="contained" onClick={onAddNewIngredient}>
            Add Ingredient
          </Button>
        </Box>
      </Stack>
    </Box>
  );
}