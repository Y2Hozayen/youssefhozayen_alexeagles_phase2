import { useState } from "react";

function ListGroup() {
  let items = ["New York", "San Franciso", "Tokyo", "London", "Alex"];

  const [selectedIndex, setselectedIndex] = useState(-1);

  items.map((item) => <li>{item}</li>);
  return (
    <>
      <h1>This is my home</h1>
      <ul className="list-group">
        {items.map((item, index) => (
          <li
            className={
              selectedIndex === index
                ? "list-group-item active"
                : "list-group-item"
            }
            key={item}
            onClick={() => {
              setselectedIndex(index);
            }}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}
export default ListGroup;
