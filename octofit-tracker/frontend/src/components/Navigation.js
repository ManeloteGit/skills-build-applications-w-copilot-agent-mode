import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navigation = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <Navbar bg="primary" expand="lg" sticky="top" className="mb-4">
      <Container>
        <Navbar.Brand as={Link} to="/" className="fw-bold">
          💪 Octofit Tracker
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            {isAuthenticated ? (
              <>
                <Nav.Link as={Link} to="/dashboard">
                  Dashboard
                </Nav.Link>
                <Nav.Link as={Link} to="/activities">
                  Actividades
                </Nav.Link>
                <Nav.Link as={Link} to="/teams">
                  Equipos
                </Nav.Link>
                <Nav.Link as={Link} to="/leaderboard">
                  Clasificación
                </Nav.Link>
                <Nav.Link as={Link} to="/profile">
                  Mi Perfil
                </Nav.Link>
                <div className="ms-3">
                  <span className="text-white me-3">
                    Bienvenido, {user?.first_name || user?.username}
                  </span>
                  <Button 
                    variant="outline-light" 
                    size="sm"
                    onClick={handleLogout}
                  >
                    Cerrar Sesión
                  </Button>
                </div>
              </>
            ) : (
              <>
                <Nav.Link as={Link} to="/login">
                  Iniciar Sesión
                </Nav.Link>
                <Nav.Link as={Link} to="/register">
                  Registrarse
                </Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;
