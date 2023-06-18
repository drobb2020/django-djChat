import { Box, CssBaseline } from '@mui/material'
import PrimaryAppBar from './template/PrimaryAppBar'

const Home = () => {
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <PrimaryAppBar />
      Home Page
    </Box>
  )
}
export default Home
