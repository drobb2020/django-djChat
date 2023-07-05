import { Box, Typography, useMediaQuery } from '@mui/material'
import { styled } from '@mui/system'
import MuiDrawer from '@mui/material/Drawer'
import { useTheme } from '@mui/material/styles'
import { useEffect, useState } from 'react'
import DrawerToggle from '../../components/PrimaryDraw/DrawerToggle'

const PrimaryDraw = () => {
  const theme = useTheme()
  const below600 = useMediaQuery('(max-width:599px')
  const [open, setOpen] = useState(!below600)

  const openedMixin = () => ({
    Transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
  })

  const closedMixin = () => ({
    Transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
    width: theme.primaryDraw.closed,
  })

  const Drawer = styled(
    MuiDrawer,
    {}
  )(({ theme, open }) => ({
    width: theme.primaryDraw.width,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(),
      '& .MuiDrawer-paper': openedMixin(),
    }),
    ...(!open && {
      ...closedMixin(),
      '& .MuiDrawer-paper': closedMixin(),
    }),
  }))

  useEffect(() => {
    setOpen(!below600)
  }, [below600])

  const handleDrawerOpen = () => {
    setOpen(true)
  }

  const handleDrawerClose = () => {
    setOpen(false)
  }

  return (
    <Drawer
      open={open}
      variant={below600 ? 'temporary' : 'permanent'}
      PaperProps={{
        sx: {
          mt: `${theme.primaryAppBar.height}px`,
          height: `calc(100vh - $(theme.primaryAppBar.height))px`,
          width: theme.primaryDraw.width,
        },
      }}
    >
      <Box>
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            right: 0,
            p: 0,
            width: open ? 'auto' : '100%',
          }}
        >
          <DrawerToggle
            open={open}
            handleDrawerOpen={handleDrawerOpen}
            handleDrawerClose={handleDrawerClose}
          />
          {[...Array(50)].map((_, i) => (
            <Typography key={i} paragraph>
              {i + 1}
            </Typography>
          ))}
        </Box>
      </Box>
    </Drawer>
  )
}
export default PrimaryDraw
