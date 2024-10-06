// File: frontend/pages/index.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  CircularProgress,
  Button,
  Box,
  IconButton
} from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';
import BookmarkIcon from '@mui/icons-material/Bookmark';
import ShareIcon from '@mui/icons-material/Share';
import Skeleton from '@mui/material/Skeleton';
import { styled } from '@mui/system';

// Define the Course type (can use TypeScript for stricter typing if desired)
/**
 * @typedef {Object} Course
 * @property {number} id - The ID of the course
 * @property {string} title - The title of the course
 * @property {string} description - The description of the course
 * @property {string} imageUrl - The URL of the course image
 */

const StyledCard = styled(Card)(({ theme }) => ({
  transition: 'transform 0.3s ease, box-shadow 0.3s ease',
  '&:hover': {
    transform: 'scale(1.05)',
    boxShadow: theme.shadows[6],
  },
}));

const Dashboard = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch personalized course recommendations for the user
    const fetchRecommendations = async () => {
      try {
        const response = await axios.get('/api/get_recommendations', {
          params: { userId: 1 }, // Assuming a hardcoded user ID for now
        });
        setRecommendations(response.data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchRecommendations();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom align="center" sx={{ fontWeight: 'bold' }}>
        Personalized Course Recommendations
      </Typography>
      {loading ? (
        <Grid container spacing={4}>
          {[...Array(6)].map((_, index) => (
            <Grid item key={index} xs={12} sm={6} md={4}>
              <Skeleton variant="rectangular" height={200} />
              <Skeleton />
              <Skeleton width="60%" />
            </Grid>
          ))}
        </Grid>
      ) : (
        <Grid container spacing={4}>
          {recommendations.map((course) => (
            <Grid item key={course.id} xs={12} sm={6} md={4}>
              <StyledCard>
                <CardMedia
                  component="img"
                  height="200"
                  image={course.imageUrl || 'https://via.placeholder.com/300'}
                  alt={course.title}
                />
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                    {course.title}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    {course.description.length > 100 ? `${course.description.substring(0, 100)}...` : course.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Button variant="contained" color="primary" size="small">
                      Enroll Now
                    </Button>
                    <Box>
                      <IconButton aria-label="add to favorites">
                        <FavoriteIcon />
                      </IconButton>
                      <IconButton aria-label="bookmark">
                        <BookmarkIcon />
                      </IconButton>
                      <IconButton aria-label="share">
                        <ShareIcon />
                      </IconButton>
                    </Box>
                  </Box>
                </CardContent>
              </StyledCard>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default Dashboard;