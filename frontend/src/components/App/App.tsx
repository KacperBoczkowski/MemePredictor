/* global IntersectionObserver */
import React, { useState, useRef, useCallback } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeart as faHeartSolid, faMeh as faMehSolid } from '@fortawesome/free-solid-svg-icons'
import { faHeart as faHeartRegular, faMeh as faMehRegular } from '@fortawesome/free-regular-svg-icons'

import useFetcher from '../Fetcher'
import * as API from '../../constants/api'

import './App.css'

function App () {
  const [page, setPage] = useState(1)
  const { favs, setFavs, loading, error } = useFetcher({ url: API.ROOT, page })

  const observer = useRef<IntersectionObserver>()
  const lastDataItemRef = useCallback(node => {
    if (loading) return
    if (observer.current) observer.current.disconnect()
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        setPage(page => page + 1)
      }
    })
    if (node) observer.current.observe(node)
  }, [loading])

  const handleClick = (id: string, reaction: string) => () => {
    setFavs(favs => favs.map(fav => fav.id === id ? { ...fav, liked: reaction === 'love' ? 1 : -1 } : fav))
  }

  return (
    <div className='container'>
      <div className='logo'>
        <span className='logo__text'>WITTY</span>
      </div>
      <div className='header' />
      <div className='sidebar' />
      <div className='main'>
        {favs.map(({ cluster, id, image, liked }, i, { length }) => (
          <div key={i} className='meme' ref={i + 1 === length ? lastDataItemRef : null}>
            <h1 className='meme__title'>{cluster}</h1>
            <img className='meme__img' src={`data:image/png;base64,${image}`} alt={`${id}`} />
            <div className='meme__footer'>
              <button className='meme__button' onClick={handleClick(id, 'love')}>
                <FontAwesomeIcon icon={liked === +1 ? faHeartSolid : faHeartRegular} />
              </button>
              <button className='meme__button' onClick={handleClick(id, 'meh')}>
                <FontAwesomeIcon icon={liked === -1 ? faMehSolid : faMehRegular} />
              </button>
            </div>
          </div>
        ))}
        {loading && 'Loading ...'}
        {error && 'Error'}
      </div>
    </div>
  )
}

export default App
