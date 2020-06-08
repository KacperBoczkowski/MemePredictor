import { useState, useEffect } from 'react'
import axios from 'axios'

interface IFetcher {
  url: string,
  page: number
}

interface IData {
  cluster: string,
  id: string,
  image: string
}

const useFetcher = ({ url, page }: IFetcher) => {
  const [data, setData] = useState<IData[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [hasMore, setHasMore] = useState(true)

  useEffect(() => {
    const fetchData = async ({ url, page }: IFetcher) => {
      setLoading(true)

      try {
        const response = await axios({ method: 'GET', url })

        setData((prevData) => [...prevData, ...response.data])
        setHasMore(true)
      } catch (e) {
        setError(e)
      } finally {
        setLoading(false)
      }
    }

    fetchData({ url, page })
  }, [url, page])

  return { data, loading, error, hasMore }
}

export default useFetcher
