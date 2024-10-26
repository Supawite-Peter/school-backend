# API Docs

## School

### Get school list

<details>
 <summary><code>GET</code> <code><b>/api/v1/schools</b></code></summary>

#### Query string

> | name | data type | description |
> |------|-----------|-------------|
> | name__iexact   | string | Exact school name to filter |
> | name__icontains   | string | Substring of school name to filter  |

#### Body

> None


#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">[<br />  {<br />    "id": 1,<br />    "name": "Thai School",<br />    "alias": "TS",<br />    "address": "Bangkok, Thailand",<br />    "classrooms_count": 3,<br />    "students_count": 6,<br />    "teachers_count": 2<br />  },<br />  ...<br />]</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Create school

<details>
 <summary><code>POST</code> <code><b>/api/v1/schools</b></code></summary>

#### Query string

> None

#### Body

> | name | type | data type | description |
> |------|------|-----------|-------------|
> | name   | required | string | Name of the school  |
> | alias   | required | string | Alias of the school  |
> | address   | required | char | Address of the school

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `201` | `application/json` | <pre lang="json"><br />{<br />  "id": 1,<br />  "name": "Thai School",<br />  "alias": "TS",<br />  "address": "Bangkok, Thailand",<br />  "classrooms_count": 0,<br />  "students_count": 0,<br />  "teachers_count": 0<br />}</pre> |
> | `400` | `application/json` | `Bad Request` |

</details>

### Get school detail

<details>
 <summary><code>GET</code> <code><b>/api/v1/schools/{id}</b></code></summary>

#### Query string

> None

#### Body

> None

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json"><br />{<br />  "id": 1,<br />  "name": "Thai School",<br />  "alias": "TS",<br />  "address": "Bangkok, Thailand",<br />  "classrooms_count": 3,<br />  "students_count": 6,<br />  "teachers_count": 2<br />}</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Update school

<details>
 <summary><code>PUT</code> <code>PATCH</code> <code><b>/api/v1/schools/{id}</b></code></summary>

#### Query string

> None

#### Body

> | name | type | data type | description |
> |------|------|-----------|-------------|
> | name   | required(PUT)/optional(PATCH) | string | Name of the school  |
> | alias   | required(PUT)/optional(PATCH) | string | Alias of the school  |
> | address   | required(PUT)/optional(PATCH) | char | Address of the school

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json"><br />{<br />  "id": 1,<br />  "name": "Thai School",<br />  "alias": "TS",<br />  "address": "Bangkok, Thailand",<br />  "classrooms_count": 0,<br />  "students_count": 0,<br />  "teachers_count": 0<br />}</pre> |
> | `404` | `application/json` | `Not Found` |
> | `400` | `application/json` | `Bad Request` |

</details>

### Delete school

<details>
 <summary><code>DELETE</code> <code><b>/api/v1/schools/{id}</b></code></summary>

#### Query string

> None

#### Body

> None

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `204` | `application/json` | `No Content`|
> | `404` | `application/json` | `Not Found` |

</details>

## Classroom

### Get classroom list

<details>
 <summary><code>GET</code> <code><b>/api/v1/classrooms</b></code></summary>

#### Query string

> | name | data type | description |
> |------|-----------|-------------|
> | school   | number | School ID to filter |

#### Body

> None


#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">[<br />  {<br />    "id": 2,<br />    "grade": 4,<br />    "room": 1,<br />    "school_detail": {<br />      "id": 1,<br />      "name": "Thai School",<br />      "alias": "TS",<br />      "address": "Bangkok, Thailand"<br />    },<br />    "teachers": [<br />      {<br />        "id": 6,<br />        "first_name": "Saranyu",<br />        "last_name": "Chansiri",<br />        "gender": "M"<br />      }<br />    ],<br />    "students": [<br />      {<br />        "id": 5,<br />        "first_name": "Chongrak",<br />        "last_name": "Kaewmanee",<br />        "gender": "M"<br />      },<br />      {<br />        "id": 10,<br />        "first_name": "Kitsakorn",<br />        "last_name": "Thawan",<br />        "gender": "M"<br />      }<br />    ]<br />  },<br />  ...<br />]</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Create classroom

<details>
 <summary><code>POST</code> <code><b>/api/v1/classrooms</b></code></summary>

#### Query string

> None

#### Body

> | name | type | data type | description |
> |------|------|-----------|-------------|
> | grade   | required | number | Grade number of the classroom  |
> | room   | required | number | Room number of the classroom  |
> | school_id   | required | char | School ID to register

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `201` | `application/json` | <pre lang="json">{<br />  "id": 2,<br />  "grade": 4,<br />  "room": 1,<br />  "school_detail": {<br />    "id": 1,<br />    "name": "Thai School",<br />    "alias": "TS",<br />    "address": "Bangkok, Thailand"<br />  },<br />  "teachers": [],<br />  "students": []<br />}</pre> |
> | `400` | `application/json` | `Bad Request` |

</details>

### Get classroom detail

<details>
 <summary><code>GET</code> <code><b>/api/v1/classrooms/{id}</b></code></summary>

#### Query string

> None

#### Body

> None

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">{<br />  "id": 2,<br />  "grade": 4,<br />  "room": 1,<br />  "school_detail": {<br />    "id": 1,<br />    "name": "Thai School",<br />    "alias": "TS",<br />    "address": "Bangkok, Thailand"<br />  },<br />  "teachers": [<br />    {<br />      "id": 6,<br />      "first_name": "Saranyu",<br />      "last_name": "Chansiri",<br />      "gender": "M"<br />    }<br />  ],<br />  "students": [<br />    {<br />      "id": 5,<br />      "first_name": "Chongrak",<br />      "last_name": "Kaewmanee",<br />      "gender": "M"<br />    },<br />    {<br />      "id": 10,<br />      "first_name": "Kitsakorn",<br />      "last_name": "Thawan",<br />      "gender": "M"<br />    }<br />  ]<br />}</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Update classroom

<details>
 <summary><code>PUT</code> <code>PATCH</code> <code><b>/api/v1/classrooms{id}</b></code></summary>

#### Query string

> None

#### Body

> | name | required | data type | description |
> |------|------|-----------|-------------|
> | grade   | required(PUT)/optional(PATCH) | number | Grade number of the classroom  |
> | room   | required(PUT)/optional(PATCH) | number | Room number of the classroom  |
> | school_id   | required(PUT) | char | School ID to register

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">{<br />  "id": 2,<br />  "grade": 4,<br />  "room": 1,<br />  "school_detail": {<br />    "id": 1,<br />    "name": "Thai School",<br />    "alias": "TS",<br />    "address": "Bangkok, Thailand"<br />  },<br />  "teachers": [],<br />  "students": []<br />}</pre> |
> | `400` | `application/json` | `Bad Request` |
> | `404` | `application/json` | `Not Found` |

</details>

### Delete classroom

<details>
 <summary><code>DELETE</code> <code><b>/api/v1/classrooms/{id}</b></code></summary>

#### Query string

> None

#### Body

> None

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `204` | `application/json` | `No Content` |
> | `404` | `application/json` | `Not Found` |

</details>

## Teacher

### Get teacher list

<details>
 <summary><code>GET</code> <code><b>/api/v1/teachers</b></code></summary>

#### Query string

> | name | data type | description |
> |------|-----------|-------------|
> | school   | number | School ID to filter |
> | classrooms | number | Classroom ID to filter |
> | first_name__iexact   | string | Exact first name to filter |
> | first_name__icontains   | string | Substring of first name to filter |
> | last_name__iexact   | string | Exact Last name to filter |
> | last_name__icontains   | string | Substring of last name to filter |
> | gender__iexact | string | Gender to filter (M/F/O) |
#### Body

> None


#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">[<br />  {<br />    "id": 6,<br />    "first_name": "Saranyu",<br />    "last_name": "Chansiri",<br />    "gender": "M",<br />    "school_detail": {<br />      "id": 1,<br />      "name": "Thai School",<br />      "alias": "TS",<br />      "address": "Bangkok, Thailand"<br />    },<br />    "classrooms": [<br />      {<br />        "id": 2,<br />        "grade": 4,<br />        "room": 1<br />      },<br />      {<br />        "id": 1,<br />        "grade": 5,<br />        "room": 2<br />      }<br />    ]<br />  },<br />  ...<br />]</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Create teacher

<details>
 <summary><code>POST</code> <code><b>/api/v1/teachers</b></code></summary>

#### Query string

> None

#### Body

> | name | type | data type | description |
> |------|------|-----------|-------------|
> | first_name   | required | string | string of first name  |
> | last_name   | required | string | string of last name  |
> | gender   | required | char | char of gender (M/F/O) => (Male, Female, Other)  |
> | school_id   | required | number | School ID to register  |
> | classrooms_id   | optional | number[] | Array of classroom id to register  |

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `201` | `application/json` | <pre lang="json">{<br />  "id": 6,<br />  "first_name": "Saranyu",<br />  "last_name": "Chansiri",<br />  "gender": "M",<br />  "school_detail": {<br />    "id": 1,<br />    "name": "Thai School",<br />    "alias": "TS",<br />    "address": "Bangkok, Thailand"<br />  },<br />  "classrooms": [<br />    {<br />      "id": 2,<br />      "grade": 4,<br />      "room": 1<br />    },<br />    {<br />      "id": 1,<br />      "grade": 5,<br />      "room": 2<br />    }<br />  ]<br />}</pre> |
> | `400` | `application/json` | `Bad Request` |

</details>

### Get teacher detail

<details>
 <summary><code>GET</code> <code><b>/api/v1/teachers/{id}</b></code></summary>

#### Query string

> None

#### Body

> None

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">{<br />  "id": 6,<br />  "first_name": "Saranyu",<br />  "last_name": "Chansiri",<br />  "gender": "M",<br />  "school_detail": {<br />    "id": 1,<br />    "name": "Thai School",<br />    "alias": "TS",<br />    "address": "Bangkok, Thailand"<br />  },<br />  "classrooms": [<br />    {<br />      "id": 2,<br />      "grade": 4,<br />      "room": 1<br />    },<br />    {<br />      "id": 1,<br />      "grade": 5,<br />      "room": 2<br />    }<br />  ]<br />}</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Update teacher

<details>
 <summary><code>PUT</code> <code>PATCH</code> <code><b>/api/v1/teachers/{id}</b></code></summary>

#### Query string

> None

#### Body

> | name | required | data type | description |
> |------|------|-----------|-------------|
> | first_name   | required(PUT)/optional(PATCH) | string | string of first name  |
> | last_name   |  required(PUT)/optional(PATCH) | string | string of last name  |
> | gender   |  required(PUT)/optional(PATCH) | char | char of gender (M/F/O) => (Male, Female, Other)  |
> | school_id   |  required(PUT)/optional(PATCH) | number | School ID to register  |
> | classrooms_id   |  required(PUT)/optional(PATCH) | number[] | Array of classroom id to register  |

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">{<br />  "id": 6,<br />  "first_name": "Saranyu",<br />  "last_name": "Chansiri",<br />  "gender": "M",<br />  "school_detail": {<br />    "id": 1,<br />    "name": "Thai School",<br />    "alias": "TS",<br />    "address": "Bangkok, Thailand"<br />  },<br />  "classrooms": [<br />    {<br />      "id": 2,<br />      "grade": 4,<br />      "room": 1<br />    },<br />    {<br />      "id": 1,<br />      "grade": 5,<br />      "room": 2<br />    }<br />  ]<br />}</pre> |
> | `400` | `application/json` | `Bad Request` |

</details>

### Delete teacher

<details>
 <summary><code>DELETE</code> <code><b>/api/v1/teachers/{id}</b></code></summary>

#### Query string

> None

#### Body

> None

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `204` | `application/json` | `No Content` |
> | `404` | `application/json` | `Not Found` |

</details>

## Student

### Get student list

<details>
 <summary><code>GET</code> <code><b>/api/v1/students</b></code></summary>

#### Query string

> | name | data type | description |
> |------|-----------|-------------|
> | school   | number | School ID to filter |
> | classrooms | number | Classroom ID to filter |
> | first_name__iexact   | string | Exact first name to filter |
> | first_name__icontains   | string | Substring of first name to filter |
> | last_name__iexact   | string | Exact Last name to filter |
> | last_name__icontains   | string | Substring of last name to filter |
> | gender__iexact | string | Gender to filter (M/F/O) |
#### Body

> None


#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">[<br />  {<br />    "id": 20,<br />    "first_name": "Alexis",<br />    "last_name": "Baker",<br />    "gender": "M",<br />    "school_detail": {<br />      "id": 2,<br />      "name": "American School",<br />      "alias": "AS",<br />      "address": "New York, USA"<br />    },<br />    "classroom_detail": {<br />      "id": 10,<br />      "grade": 9,<br />      "room": 3<br />    }<br />  },<br />  ...<br />]</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Create student

<details>
 <summary><code>POST</code> <code><b>/api/v1/students</b></code></summary>

#### Query string

> None

#### Body

> | name | required | data type | description |
> |------|------|-----------|-------------|
> | first_name   | required | string | string of first name  |
> | last_name   | required | string | string of last name  |
> | gender   | required | char | char of gender (M/F/O) => (Male, Female, Other)  |
> | classroom_id   | required | number | Classroom id to register  |

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `201` | `application/json` | <pre lang="json">{<br />  "id": 20,<br />  "first_name": "Alexis",<br />  "last_name": "Baker",<br />  "gender": "M",<br />  "school_detail": {<br />    "id": 2,<br />    "name": "American School",<br />    "alias": "AS",<br />    "address": "New York, USA"<br />  },<br />  "classroom_detail": {<br />    "id": 10,<br />    "grade": 9,<br />    "room": 3<br />  }<br />}</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Get student detail

<details>
 <summary><code>GET</code> <code><b>/api/v1/students/{id}</b></code></summary>

#### Query string

> None

#### Body

> None

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">{<br />  "id": 20,<br />  "first_name": "Alexis",<br />  "last_name": "Baker",<br />  "gender": "M",<br />  "school_detail": {<br />    "id": 2,<br />    "name": "American School",<br />    "alias": "AS",<br />    "address": "New York, USA"<br />  },<br />  "classroom_detail": {<br />    "id": 10,<br />    "grade": 9,<br />    "room": 3<br />  }<br />}</pre> |
> | `404` | `application/json` | `NotFound` |

</details>

### Update student 

<details>
 <summary><code>PUT</code> <code>PATCH</code> <code><b>/api/v1/students/{id}</b></code></summary>

#### Query string

> None

#### Body

> | name | required | data type | description |
> |------|------|-----------|-------------|
> | first_name   | required(PUT)/optional(PATCH) | string | string of first name  |
> | last_name   | required(PUT)/optional(PATCH) | string | string of last name  |
> | gender   | required(PUT)/optional(PATCH) | char | char of gender (M/F/O) => (Male, Female, Other)  |
> | classroom_id   | required(PUT)/optional(PATCH) | number | Classroom id to register  |

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `200` | `application/json` | <pre lang="json">{<br />  "id": 20,<br />  "first_name": "Alexis",<br />  "last_name": "Baker",<br />  "gender": "M",<br />  "school_detail": {<br />    "id": 2,<br />    "name": "American School",<br />    "alias": "AS",<br />    "address": "New York, USA"<br />  },<br />  "classroom_detail": {<br />    "id": 10,<br />    "grade": 9,<br />    "room": 3<br />  }<br />}</pre> |
> | `400` | `application/json` | `Bad Request` |
> | `404` | `application/json` | `Not Found` |

</details>

### Delete student

<details>
 <summary><code>DELETE</code> <code><b>/api/v1/students/{id}</b></code></summary>

#### Query string

> None

#### Body

> None

#### Responses

> | http code | content-type | response |
> |-----------|--------------|----------|
> | `204` | `application/json` | `No Content` |
> | `404` | `application/json` | `Not Found` |

</details>