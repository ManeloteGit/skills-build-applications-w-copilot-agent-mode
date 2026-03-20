import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Spinner } from 'react-bootstrap';
import { useAuth } from '../hooks/useAuth';
import { userService } from '../services/api';

const Profile = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [activeTab, setActiveTab] = useState('profile');

  const [profileData, setProfileData] = useState({
    first_name: '',
    last_name: '',
    height_cm: '',
    weight_kg: '',
    age: '',
    gender: '',
    fitness_level: '',
    bio: '',
  });

  const [passwordData, setPasswordData] = useState({
    old_password: '',
    new_password: '',
    new_password2: '',
  });

  useEffect(() => {
    if (user) {
      setProfileData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        height_cm: user.height_cm || '',
        weight_kg: user.weight_kg || '',
        age: user.age || '',
        gender: user.gender || '',
        fitness_level: user.fitness_level || '',
        bio: user.bio || '',
      });
      setLoading(false);
    }
  }, [user]);

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setSaving(true);

    try {
      await userService.updateProfile(user.id, profileData);
      setSuccess('Perfil actualizado correctamente');
    } catch (err) {
      setError('Error al actualizar el perfil');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (passwordData.new_password !== passwordData.new_password2) {
      setError('Las nuevas contraseñas no coinciden');
      return;
    }

    setSaving(true);

    try {
      await userService.changePassword(passwordData);
      setSuccess('Contraseña actualizada correctamente');
      setPasswordData({
        old_password: '',
        new_password: '',
        new_password2: '',
      });
    } catch (err) {
      setError(err.response?.data?.old_password?.[0] || 'Error al cambiar la contraseña');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '70vh' }}>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando...</span>
        </Spinner>
      </Container>
    );
  }

  const bmi = profileData.height_cm && profileData.weight_kg
    ? (profileData.weight_kg / ((profileData.height_cm / 100) ** 2)).toFixed(1)
    : null;

  return (
    <Container>
      <Row className="mb-4">
        <Col>
          <h1 className="display-5 fw-bold">👤 Mi Perfil</h1>
        </Col>
      </Row>

      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')} dismissible>{success}</Alert>}

      <Row>
        <Col md={3} className="mb-4">
          <Card className="shadow-sm">
            <Card.Body className="text-center">
              <div style={{ fontSize: '60px', marginBottom: '15px' }}>👤</div>
              <h5>{user?.first_name} {user?.last_name}</h5>
              <p className="text-muted">@{user?.username}</p>
              <hr />
              <p className="small">
                <strong>Email:</strong> {user?.email}
              </p>
              {bmi && (
                <p className="small">
                  <strong>IMC:</strong> {bmi}
                </p>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col md={9}>
          <Card className="shadow-sm">
            <Card.Header className="bg-primary text-white">
              <div className="btn-group w-100" role="group">
                <input 
                  type="radio" 
                  className="btn-check" 
                  id="profileTab" 
                  value="profile"
                  checked={activeTab === 'profile'}
                  onChange={(e) => setActiveTab(e.target.value)}
                />
                <label className="btn btn-outline-light" htmlFor="profileTab">
                  Mi Información
                </label>
                
                <input 
                  type="radio" 
                  className="btn-check" 
                  id="passwordTab" 
                  value="password"
                  checked={activeTab === 'password'}
                  onChange={(e) => setActiveTab(e.target.value)}
                />
                <label className="btn btn-outline-light" htmlFor="passwordTab">
                  Cambiar Contraseña
                </label>
              </div>
            </Card.Header>

            <Card.Body>
              {activeTab === 'profile' && (
                <Form onSubmit={handleUpdateProfile}>
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Nombre</Form.Label>
                        <Form.Control
                          type="text"
                          name="first_name"
                          value={profileData.first_name}
                          onChange={handleProfileChange}
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Apellido</Form.Label>
                        <Form.Control
                          type="text"
                          name="last_name"
                          value={profileData.last_name}
                          onChange={handleProfileChange}
                        />
                      </Form.Group>
                    </Col>
                  </Row>

                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Altura (cm)</Form.Label>
                        <Form.Control
                          type="number"
                          step="0.1"
                          name="height_cm"
                          value={profileData.height_cm}
                          onChange={handleProfileChange}
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Peso (kg)</Form.Label>
                        <Form.Control
                          type="number"
                          step="0.1"
                          name="weight_kg"
                          value={profileData.weight_kg}
                          onChange={handleProfileChange}
                        />
                      </Form.Group>
                    </Col>
                  </Row>

                  <Row>
                    <Col md={4}>
                      <Form.Group className="mb-3">
                        <Form.Label>Edad</Form.Label>
                        <Form.Control
                          type="number"
                          name="age"
                          value={profileData.age}
                          onChange={handleProfileChange}
                        />
                      </Form.Group>
                    </Col>
                    <Col md={4}>
                      <Form.Group className="mb-3">
                        <Form.Label>Género</Form.Label>
                        <Form.Select
                          name="gender"
                          value={profileData.gender}
                          onChange={handleProfileChange}
                        >
                          <option value="">Seleccionar</option>
                          <option value="M">Masculino</option>
                          <option value="F">Femenino</option>
                          <option value="O">Otro</option>
                        </Form.Select>
                      </Form.Group>
                    </Col>
                    <Col md={4}>
                      <Form.Group className="mb-3">
                        <Form.Label>Nivel de Aptitud</Form.Label>
                        <Form.Select
                          name="fitness_level"
                          value={profileData.fitness_level}
                          onChange={handleProfileChange}
                        >
                          <option value="beginner">Principiante</option>
                          <option value="intermediate">Intermedio</option>
                          <option value="advanced">Avanzado</option>
                          <option value="athlete">Atleta</option>
                        </Form.Select>
                      </Form.Group>
                    </Col>
                  </Row>

                  <Form.Group className="mb-3">
                    <Form.Label>Biografía</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={4}
                      name="bio"
                      value={profileData.bio}
                      onChange={handleProfileChange}
                      placeholder="Cuéntanos sobre ti..."
                    />
                  </Form.Group>

                  <Button 
                    variant="primary" 
                    type="submit"
                    disabled={saving}
                  >
                    {saving ? 'Guardando...' : 'Guardar Cambios'}
                  </Button>
                </Form>
              )}

              {activeTab === 'password' && (
                <Form onSubmit={handleChangePassword}>
                  <Form.Group className="mb-3">
                    <Form.Label>Contraseña Actual</Form.Label>
                    <Form.Control
                      type="password"
                      name="old_password"
                      value={passwordData.old_password}
                      onChange={handlePasswordChange}
                      required
                    />
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Nueva Contraseña</Form.Label>
                    <Form.Control
                      type="password"
                      name="new_password"
                      value={passwordData.new_password}
                      onChange={handlePasswordChange}
                      required
                    />
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Confirmar Nueva Contraseña</Form.Label>
                    <Form.Control
                      type="password"
                      name="new_password2"
                      value={passwordData.new_password2}
                      onChange={handlePasswordChange}
                      required
                    />
                  </Form.Group>

                  <Button 
                    variant="primary" 
                    type="submit"
                    disabled={saving}
                  >
                    {saving ? 'Cambiando...' : 'Cambiar Contraseña'}
                  </Button>
                </Form>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Profile;
