// This is the main App component
// This file defines the structure of the application
// The App component serves as the root of the application
import Login from "./components/Login";
import Inventory from "./components/Inventory";
import UserRights from "./components/UserRights";

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/user-rights" element={<UserRights />} />
      </Routes>
    </div>
  );
}

export default App;