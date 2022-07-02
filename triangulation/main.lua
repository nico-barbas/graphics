local function sub(a, b)
    return {
        x = a.x - b.x,
        y = a.y - b.y,
    }
end

local function cross(a, b)
    return (a.x * b.y - b.x * a.y)
end

local function pointInTriangle(tInfo, point)
    local result = false

    -- local origin_to_point = sub(point, tInfo.points[1])
    -- local cross_ap = cross(
    --     tInfo.vectors.a,
    --     origin_to_point
    -- )
    -- local signed_cross = cross_ap > 0

    -- if signed_cross == tInfo.signed_cross then
    --     local next_a = sub(tInfo.points[1], tInfo.points[3])
    --     local next_to_point = sub(
    --         point,
    --         tInfo.points[3]
    --     )
    --     local next_cross_ap = cross(
    --         next_a,
    --         next_to_point
    --     )
    --     local next_signed_cross = next_cross_ap > 0
    --     print(next_signed_cross, tInfo.signed_cross)
    --     if not (next_signed_cross == tInfo.signed_cross) then
    --         result = true
    --     end
    -- end

    local p0_to_point = sub(point, tInfo.points[1])
    local cross_1 = cross(
        tInfo.vectors.a,
        p0_to_point
    )
    if not ((cross_1 >= 0) == tInfo.signed_cross) then
        return result
    end

    local cross_2 = cross(
        p0_to_point,
        tInfo.vectors.b
    )
    if not ((cross_2 >= 0) == tInfo.signed_cross) then
        return result
    end


    local next_a = sub(tInfo.points[1], tInfo)
    local next_b
    local p2_to_point

    return result
end

local polygon = {
    { x = 1, y = 1 },
    { x = 2, y = 0 },
    { x = 2.5, y = 0.5 },
    { x = 2, y = 1 },
    { x = 2.5, y = 1.5 },
    { x = 2, y = 2 },
}

local len = #polygon
local ordering = "clockwise"

local INF           = math.huge
local testing_point = { x = -INF, y = INF }
local testing_index = -1
for i, point in ipairs(polygon) do
    if point.y < testing_point.y then
        testing_point = point
        testing_index = i
    elseif point.y == testing_point.y then
        if point.x > testing_point.x then
            testing_point = point
            testing_index = i
        end
    end
end

if testing_index == -1 then
    print("ERROR")
    return
end

local ti1 = (testing_index - 1) % len
if ti1 < 1 then
    ti1 = 4
end

local ti2 = (testing_index + 1)
if ti2 > len then
    ti2 = 1
end

local tp1 = polygon[ti1]
local tp2 = polygon[ti2]

local ta = sub(tp1, testing_point)
local tb = sub(tp2, testing_point)
if cross(ta, tb) < 0 then
    ordering = "counter-clockwise"
end

print(ordering)

local triangleInfo = {
    points = { nil, nil, nil },
    vectors = { a = nil, b = nil },
    signed_cross = nil,
}

local open_set = {
    count = #polygon,
    indices = {},
}

for i, _ in ipairs(polygon) do
    open_set.indices[i] = i
end

function open_set:remove(r_index)
    for i = 1, self.count do
        local index = self.indices[i]
        if index == r_index then
            self.indices[i] = self.indices[self.count]
            self.count = self.count - 1
        end
    end
end

function open_set:contains(r_index)
    local result = false
    for i = 1, self.count do
        local index = self.indices[i]
        if index == r_index then
            result = true
            break
        end
    end
    return result
end

local triangulated_polygon = {
    tri_count = 0,
    triangles = {},
}

function triangulated_polygon:add(i0, i1, i2)
    self.tri_count = self.tri_count + 1
    self.triangles[self.tri_count] = { i0, i1, i2 }
end

for i, p0 in ipairs(polygon) do
    if open_set.count == 3 then
        -- local li0 = open_set.indices[1]
        -- local li1 = open_set.indices[2]
        -- local li2 = open_set.indices[3]

        -- local lp0 = polygon[li0]
        -- local lp1 = polygon[li1]
        -- local lp2 = polygon[li2]

        -- local la = sub(lp1, lp0)
        -- local lb = sub(lp2, lp0)
        -- local cross_last_ab = cross(la, lb)
        -- if ordering == "clockwise" then
        --     if cross_last_ab < 0 then
        --         local temp = li1
        --         li1 = li2
        --         li2 = temp
        --     end
        --     triangulated_polygon:add(li0, li1, li2)
        -- elseif ordering == "counter-clockwise" then
        --     if cross_last_ab > 0 then
        --         local temp = li1
        --         li1 = li2
        --         li2 = temp
        --     end
        --     triangulated_polygon:add(li0, li2, li1)
        -- end
        break
    end

    if open_set:contains(i) then
        local i1 = (i - 1) % len
        if i1 < 1 then
            i1 = len
        end

        local i2 = (i + 1)
        if i2 > len then
            i2 = 1
        end

        print("p0 is:", i, "p1 is:", i1, "p2 is:", i2)

        local p1 = polygon[i1]
        local p2 = polygon[i2]

        local a = sub(p1, p0)
        local b = sub(p2, p0)

        local cross_ab = cross(a, b)
        local is_ear = false
        if ordering == "clockwise" then
            if cross_ab > 0 then
                is_ear = true
                triangleInfo.points[1] = p0
                triangleInfo.points[2] = p1
                triangleInfo.points[3] = p2
                triangleInfo.vectors.a = a
                triangleInfo.vectors.b = b
                triangleInfo.signed_cross = true
            end
        elseif ordering == "counter-clockwise" then
            if cross_ab < 0 then
                is_ear = true
                triangleInfo.points[1] = p0
                triangleInfo.points[2] = p1
                triangleInfo.points[3] = p2
                triangleInfo.vectors.a = a
                triangleInfo.vectors.b = b
                triangleInfo.signed_cross = false
            end
        end

        if is_ear then
            for j, next_point in ipairs(polygon) do
                if not (j == i or j == i1 or j == i2) then
                    local point_in_ear = pointInTriangle(
                        triangleInfo,
                        next_point
                    )
                    if point_in_ear then
                        print(j, "is in ear", i, i1, i2)
                        is_ear = false
                        break
                    end
                end
            end
        end

        if is_ear then
            print(
                "[", i, i1, i2, "] is a possible ear!"
            )
            open_set:remove(i)
            if ordering == "clockwise" then
                triangulated_polygon:add(i, i1, i2)
            elseif ordering == "counter-clockwise" then
                triangulated_polygon:add(i, i2, i1)
            end
        end
    end
end

print("Triangle count:", triangulated_polygon.tri_count)
for i = 1, triangulated_polygon.tri_count do
    local triangle = triangulated_polygon.triangles[i]
    print(
        "- [", triangle[1], triangle[2], triangle[3], "]"
    )
end


local colors = {
    { math.random(), math.random(), math.random(), 1 },
    { math.random(), math.random(), math.random(), 1 },
    { math.random(), math.random(), math.random(), 1 },
    { math.random(), math.random(), math.random(), 1 },
    { math.random(), math.random(), math.random(), 1 },
}

local scale = 100

function love.draw()
    for i = 1, triangulated_polygon.tri_count do
        local clr = colors[i % #colors + 1]
        love.graphics.setColor(clr[1], clr[2], clr[3], clr[4])
        local triangle = triangulated_polygon.triangles[i]
        local p0 = polygon[ triangle[1] ]
        local p1 = polygon[ triangle[2] ]
        local p2 = polygon[ triangle[3] ]
        love.graphics.line(p0.x * scale, p0.y * scale, p1.x * scale, p1.y * scale)
        love.graphics.line(p0.x * scale, p0.y * scale, p2.x * scale, p2.y * scale)
        love.graphics.line(p1.x * scale, p1.y * scale, p2.x * scale, p2.y * scale)
    end
end
