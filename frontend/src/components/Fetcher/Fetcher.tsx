import { useState, useEffect } from 'react'
import axios from 'axios'

import { N } from '../../constants/items'
import { IFav, IFetcher } from '../../intefaces'

const useFetcher = ({ url, page }: IFetcher) => {
  const [favs, setFavs] = useState<IFav[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)

      try {
        console.log(favs.slice(-N))
        const response = await axios({ method: 'POST', url, data: favs.slice(-N) })

        setFavs((prevData) => [...prevData, ...response.data])
      } catch (e) {
        setError(e)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [url, page])

  return { favs, setFavs, loading, error }
}

export default useFetcher
