import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { Ingredient } from '../ingredients';



export default function IngredientsTable({ingredients}: {ingredients: Ingredient[]}) {
  return (
    <TableContainer component={Paper}>
      <Table stickyHeader sx={{ minWidth: 650 }} aria-label="ingredients table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell align="right">Unit(mL, g, etc.)</TableCell>
            <TableCell align="right">Calories</TableCell>
            <TableCell align="right">Protein (g)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {ingredients.map((ingredient) => (
            <TableRow
              key={ingredient.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {ingredient.name}
              </TableCell>
              <TableCell align="right">{ingredient.quantity_unit}</TableCell>
              <TableCell align="right">{ingredient.calories}</TableCell>
              <TableCell align="right">{ingredient.protein}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}