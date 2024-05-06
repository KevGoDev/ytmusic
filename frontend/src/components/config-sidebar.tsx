import { Egg, MenuBook, RamenDining } from "@mui/icons-material";

const SIDEBAR_ITEMS = [
    {"title": "Plans", "icon": <RamenDining />, "path": "/plans"},
    {"title": "Meals", "icon": <MenuBook />, "path": "/meals"},
    {"title": "Ingredients", "icon": <Egg />, "path": "/ingredients"},
];

export default SIDEBAR_ITEMS;
