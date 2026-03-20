import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Spinner, Alert, Table } from 'react-bootstrap';
import { leaderboardService } from '../services/api';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      setError('');
      const response = await leaderboardService.getCurrentWeek();
      setLeaderboard(response.data.results || response.data || []);
    } catch (err) {
      setError('Error al cargar la clasificación');
      console.error(err);
    } finally {
      setLoading(false);
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

  return (
    <Container>
      <Row className="mb-4">
        <Col>
          <h1 className="display-5 fw-bold">🏆 Clasificación Semanal</h1>
          <p className="text-muted">Compite con otros usuarios y sube en el ranking</p>
        </Col>
      </Row>

      {error && <Alert variant="danger">{error}</Alert>}

      <Row>
        <Col>
          <Card className="shadow-sm">
            <Card.Body className="p-0">
              {leaderboard.length === 0 ? (
                <div className="p-4 text-center text-muted">
                  Sin datos de clasificación aún. Registra actividades para aparecer en el ranking.
                </div>
              ) : (
                <Table responsive className="mb-0">
                  <thead className="table-light">
                    <tr>
                      <th style={{ width: '50px' }}>Posición</th>
                      <th>Usuario</th>
                      <th>Puntos</th>
                      <th>Actividades</th>
                      <th>Duración</th>
                      <th>Calorías</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leaderboard.map((entry, index) => (
                      <tr key={entry.id} className={index === 0 ? 'table-success' : index === 1 ? 'table-info' : index === 2 ? 'table-warning' : ''}>
                        <td>
                          <h5 className="mb-0">
                            {index === 0 && '🥇'}
                            {index === 1 && '🥈'}
                            {index === 2 && '🥉'}
                            {index > 2 && `#${entry.rank || index + 1}`}
                          </h5>
                        </td>
                        <td>
                          <strong>{entry.user_username}</strong>
                        </td>
                        <td>
                          <h6 className="mb-0">
                            {entry.points || 0}
                          </h6>
                        </td>
                        <td>{entry.activities_count || 0}</td>
                        <td>{entry.total_duration_minutes || 0} min</td>
                        <td>{entry.total_calories || 0} kcal</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={3} className="mb-3">
          <Card className="text-center shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Participantes</h6>
              <h2 className="mb-0">{leaderboard.length}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3} className="mb-3">
          <Card className="text-center shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Actividades</h6>
              <h2 className="mb-0">
                {leaderboard.reduce((sum, entry) => sum + (entry.activities_count || 0), 0)}
              </h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3} className="mb-3">
          <Card className="text-center shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Minutos Totales</h6>
              <h2 className="mb-0">
                {leaderboard.reduce((sum, entry) => sum + (entry.total_duration_minutes || 0), 0)}
              </h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3} className="mb-3">
          <Card className="text-center shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Calorías Totales</h6>
              <h2 className="mb-0">
                {leaderboard.reduce((sum, entry) => sum + (entry.total_calories || 0), 0)}
              </h2>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Leaderboard;
